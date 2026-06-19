from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from core.llm.response import LLMResponse


class LLMProvider(ABC):

    @abstractmethod
    async def invoke(
        self,
        prompt: str,
    ) -> LLMResponse:
        pass


    @abstractmethod
    async def structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        pass