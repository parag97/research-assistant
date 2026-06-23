import time
from typing import Type

from pydantic import BaseModel

from langchain_openrouter import ChatOpenRouter

from core.llm.base import LLMProvider
from core.llm.models import LLMProviderType
from core.llm.response import LLMResponse
from tools.base import BaseTool
from tools.models import ToolCall, ToolPlan


class OpenRouterProvider(LLMProvider):
    """
    LLMProvider implementation backed by a local Ollama instance.

    Supports plain text generation, structured output via JSON schema,
    and tool-call binding using LangChain's bind_tools interface.
    """

    def __init__(
        self,
        model: str,
        api_key: str
        
    ) -> None:

        self.model = model
        self.client = ChatOpenRouter(
            model=self.model,
            openrouter_api_key=api_key,
            temperature=0.0,
        )

    
    async def invoke(self, prompt: str) -> LLMResponse:
        """Send a plain text prompt and return a normalised LLMResponse."""

        start = time.perf_counter()
        # with runtime.tracer.span("gemini_invoke"):
        response = await self.client.ainvoke(prompt)
        latency_ms = (time.perf_counter() - start) * 1000

        return LLMResponse(
            content=response.content,
            model=self.model,
            provider=LLMProviderType.OLLAMA,
            latency_ms=round(latency_ms, 2),
        )

    async def structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """
        Send a prompt and parse the response into a Pydantic schema.
        Uses LangChain's with_structured_output for JSON enforcement.
        """

        structured_llm = self.client.with_structured_output(schema)
        return await structured_llm.ainvoke(prompt)

    async def invoke_with_tools(
        self,
        prompt: str,
        tools: list[BaseTool],
    ) -> ToolPlan:
        """
        Send a prompt with tool definitions and return a ToolPlan.
        Uses LangChain's bind_tools to pass OpenAI-style function schemas.
        """

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

        client_with_tools = self.client.bind_tools(tool_schemas)
        response = await client_with_tools.ainvoke(prompt)

        tool_calls = [
            ToolCall(tool_name=tc["name"], arguments=tc["args"])
            for tc in (response.tool_calls or [])
        ]

        return ToolPlan(tool_calls=tool_calls)
