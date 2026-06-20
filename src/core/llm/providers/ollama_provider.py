import time
from typing import Type

from pydantic import BaseModel

from langchain_ollama import ChatOllama

from core.llm.base import LLMProvider
from core.llm.response import LLMResponse
from core.llm.models import LLMProviderType
from tools.base import BaseTool
from tools.models import ToolPlan, ToolCall


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
    ):
        self.model = model

        self.client = ChatOllama(
            model=model,
            base_url=base_url,
        )

    async def invoke(
        self,
        prompt: str,
    ) -> LLMResponse:

        start = time.perf_counter()

        response = await self.client.ainvoke(prompt)

        latency = (time.perf_counter() - start) * 1000

        return LLMResponse(
            content=response.content,
            model=self.model,
            provider=LLMProviderType.OLLAMA,
            latency_ms=round(latency, 2),
        )

    async def structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:

        structured_llm = self.client.with_structured_output(schema)

        return await structured_llm.ainvoke(prompt)

    async def invoke_with_tools(
        self,
        prompt: str,
        tools: list[BaseTool],
    ) -> ToolPlan:

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
            ToolCall(
                tool_name=tc["name"],
                arguments=tc["args"],
            )
            for tc in (response.tool_calls or [])
        ]

        return ToolPlan(tool_calls=tool_calls)
