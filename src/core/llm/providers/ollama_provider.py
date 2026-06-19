import time
from typing import Type

from pydantic import BaseModel

from langchain_ollama import ChatOllama

from core.llm.base import LLMProvider
from core.llm.response import LLMResponse
from core.llm.models import LLMProviderType


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
