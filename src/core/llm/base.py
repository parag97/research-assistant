from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from core.llm.response import LLMResponse
from tools.base import BaseTool
from tools.models import ToolPlan


class LLMProvider(ABC):
    """
    Abstract base class for all LLM provider implementations.

    Concrete implementations (OllamaProvider, GoogleProvider, etc.) must
    implement all three methods. The interface is intentionally minimal —
    providers handle their own auth, retries, and serialisation internally.
    """

    @abstractmethod
    async def invoke(self, prompt: str) -> LLMResponse:
        """Send a plain text prompt and return a normalised LLMResponse."""

    @abstractmethod
    async def structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """
        Send a prompt and parse the response into a Pydantic schema.

        Used for structured output (JSON-mode) calls where the response
        must conform to a specific data model.
        """

    @abstractmethod
    async def invoke_with_tools(
        self,
        prompt: str,
        tools: list[BaseTool],
    ) -> ToolPlan:
        """
        Send a prompt with tool definitions and return a ToolPlan.

        The provider is responsible for converting BaseTool descriptors
        into its own function-calling format.
        """
