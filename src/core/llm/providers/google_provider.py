import time

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from core.llm.base import LLMProvider
from core.llm.response import LLMResponse


class GoogleProvider(LLMProvider):

    def __init__(
        self,
        model: str,
        api_key: str,
    ):
        self.model = model

        self.client = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
        )

    async def invoke(
        self,
        prompt: str,
    ) -> LLMResponse:

        start_time = time.perf_counter()

        response = await self.client.ainvoke(prompt)

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return LLMResponse(
            content=response.content,
            model=self.model,
            provider="google",
            latency_ms=round(latency_ms, 2),
        )