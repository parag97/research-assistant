import time
from typing import Type

from pydantic import BaseModel

from opentelemetry.trace import get_current_span
from core.observability.tracer import Tracer

from langchain_openrouter import ChatOpenRouter

from core.llm.base import LLMProvider
from core.llm.models import LLMProviderType
from core.llm.response import LLMResponse
from tools.base import BaseTool
from tools.models import ToolCall, ToolPlan


# ---------------------------------------------------------------------------
# Langfuse Generation attributes
# ---------------------------------------------------------------------------
# Langfuse reads specific OTel span attributes to render a span as a
# "generation" in its UI — showing prompt, completion, token usage, cost etc.
#
# The full attribute reference is at:
# https://langfuse.com/docs/opentelemetry/get-started#generation-attributes
#
# Key ones we use:
#   langfuse.span.type          = "GENERATION"  ← tells Langfuse this is an LLM call
#   gen_ai.system               = provider name (e.g. "openai", "openrouter")
#   gen_ai.request.model        = model string sent to the API
#   gen_ai.response.model       = model string returned in the response
#   gen_ai.usage.input_tokens   = prompt token count
#   gen_ai.usage.output_tokens  = completion token count
#   gen_ai.prompt               = the actual prompt text (shown in Langfuse UI)
#   gen_ai.completion           = the actual response text
# ---------------------------------------------------------------------------

_GENERATION = "GENERATION"


def _set_generation_attributes(
    prompt: str,
    model: str,
    completion: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    latency_ms: float | None = None,
) -> None:
    """
    Attach Langfuse generation attributes to the currently active OTel span.

    Must be called from inside a `with tracer.span(...)` block so there
    IS a current span. get_current_span() returns a no-op span if called
    outside a span context — attributes set on it are silently discarded,
    so this is safe to call unconditionally.

    We keep this as a free function (not a method) so it can be reused
    identically across invoke(), structured(), and invoke_with_tools().
    """
    span = get_current_span()

    # This single attribute is what makes Langfuse treat this span as a
    # generation rather than a plain trace span. Without it, Langfuse
    # shows it as a generic event with no LLM-specific UI.
    span.set_attribute("langfuse.span.type", _GENERATION)

    # gen_ai.* attributes follow the OpenTelemetry GenAI semantic conventions
    # (https://opentelemetry.io/docs/specs/semconv/gen-ai/). Langfuse reads
    # these to populate the model, token, and cost fields in the UI.
    span.set_attribute("gen_ai.system", "openrouter")
    span.set_attribute("gen_ai.request.model", model)

    # Prompt and completion are stored as span attributes so Langfuse can
    # display the full conversation in its generation detail view.
    span.set_attribute("gen_ai.prompt", prompt)

    if completion is not None:
        span.set_attribute("gen_ai.completion", completion)
        span.set_attribute("gen_ai.response.model", model)

    # Token counts drive cost estimation in Langfuse's analytics dashboard.
    # They're optional — if the provider doesn't return them we skip them.
    if input_tokens is not None:
        span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
    if output_tokens is not None:
        span.set_attribute("gen_ai.usage.output_tokens", output_tokens)

    # latency_ms is a custom attribute — not a Langfuse standard but useful
    # to have on the span for debugging slow calls in the trace waterfall.
    if latency_ms is not None:
        span.set_attribute("llm.latency_ms", round(latency_ms, 2))


class OpenRouterProvider(LLMProvider):
    """
    LLMProvider implementation backed by OpenRouter.

    Supports plain text generation, structured output via JSON schema,
    and tool-call binding using LangChain's bind_tools interface.

    Every LLM call opens an OTel span and attaches Langfuse generation
    attributes so each call appears as a tracked generation in Langfuse,
    nested under the parent workflow/agent span.
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        tracer: Tracer,
    ) -> None:
        self.model = model
        self._tracer = tracer
        self.client = ChatOpenRouter(
            model=self.model,
            openrouter_api_key=api_key,
            temperature=0.0,
        )

    async def invoke(self, prompt: str) -> LLMResponse:
        """
        Send a plain text prompt and return a normalised LLMResponse.

        Span tree in Langfuse:
            [parent workflow span]
              └── OpenRouterInvoke   ← this span, type=GENERATION
        """
        with self._tracer.span("OpenRouterInvoke"):
            start = time.perf_counter()
            response = await self.client.ainvoke(prompt)
            latency_ms = (time.perf_counter() - start) * 1000

            # LangChain returns token usage in response.usage_metadata when
            # the provider reports it. We extract it here so Langfuse can
            # show token counts and estimated cost per generation.
            usage = getattr(response, "usage_metadata", None)
            input_tokens = usage.get("input_tokens") if usage else None
            output_tokens = usage.get("output_tokens") if usage else None

            _set_generation_attributes(
                prompt=prompt,
                model=self.model,
                completion=str(response.content),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
            )

            return LLMResponse(
                content=response.content,
                model=self.model,
                provider=LLMProviderType.OPEN_ROUTER,
                latency_ms=round(latency_ms, 2),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

    async def structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """
        Send a prompt and parse the response into a Pydantic schema.

        Uses LangChain's with_structured_output for JSON enforcement.
        The schema name is recorded as a custom attribute so you can filter
        by schema type in Langfuse.
        """
        with self._tracer.span("OpenRouterStructured"):
            # Record the schema name before the call so it's on the span
            # even if the call raises an exception.
            span = get_current_span()
            span.set_attribute("llm.schema", schema.__name__)

            start = time.perf_counter()
            structured_llm = self.client.with_structured_output(schema)
            result = await structured_llm.ainvoke(prompt)
            latency_ms = (time.perf_counter() - start) * 1000

            _set_generation_attributes(
                prompt=prompt,
                model=self.model,
                # Serialize the structured result back to a string so
                # Langfuse can show what the model actually returned.
                completion=result.model_dump_json() if hasattr(result, "model_dump_json") else str(result),
                latency_ms=latency_ms,
            )

            return result

    async def invoke_with_tools(
        self,
        prompt: str,
        tools: list[BaseTool],
    ) -> ToolPlan:
        """
        Send a prompt with tool definitions and return a ToolPlan.

        The tool names selected by the model are recorded as a span
        attribute so you can see tool selection patterns in Langfuse.
        """
        with self._tracer.span("OpenRouterToolCall"):
            span = get_current_span()
            span.set_attribute("tool.available_count", len(tools))

            tool_schemas = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.schema,
                    },
                }
                for tool in tools
            ]

            start = time.perf_counter()
            client_with_tools = self.client.bind_tools(tool_schemas)
            response = await client_with_tools.ainvoke(prompt)
            latency_ms = (time.perf_counter() - start) * 1000

            tool_calls = [
                ToolCall(tool_name=tc["name"], arguments=tc["args"])
                for tc in (response.tool_calls or [])
            ]

            # Record which tools the model chose — useful for debugging
            # cases where the model selects the wrong tool.
            selected_names = [tc.tool_name for tc in tool_calls]
            span.set_attribute("tool.selected_count", len(tool_calls))
            span.set_attribute("tool.selected_names", str(selected_names))

            _set_generation_attributes(
                prompt=prompt,
                model=self.model,
                # The "completion" for a tool call is the list of selected
                # tools and their arguments, not free text.
                completion=str([tc.model_dump() for tc in tool_calls]),
                latency_ms=latency_ms,
            )

            return ToolPlan(tool_calls=tool_calls)
