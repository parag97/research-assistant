from abc import ABC, abstractmethod

from core.llm.response import LLMResponse


class LLMProvider(ABC):

    @abstractmethod
    async def invoke(
        self,
        prompt: str,
    ) -> LLMResponse:
        pass