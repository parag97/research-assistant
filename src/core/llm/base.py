from tools.models import ToolPlan
from tools.base import BaseTool
from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from core.llm.response import LLMResponse
from tools.base import BaseTool
from tools.models import ToolPlan
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
    @abstractmethod
    
    async def invoke_with_tools(
        self,
        prompt: str,
        tools:list[BaseTool]
    )-> ToolPlan:
        pass