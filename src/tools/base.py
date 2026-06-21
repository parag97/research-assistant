from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseTool(ABC):
    """
    Abstract base class for all tools available to agents.

    Tools are discrete, reusable capabilities (fetch URL, run calculator,
    get datetime, etc.) that agents can invoke during research planning.

    Each tool exposes a name, a description (used by the LLM to decide
    whether to call it), and an input_model that defines and validates
    the arguments the tool accepts.

    Concrete tools must implement name, description, input_model, and execute.
    The schema property is derived automatically from input_model.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier used to look up this tool in the registry."""

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Natural-language description passed to the LLM during tool planning.
        Should clearly state what the tool does and when to use it.
        """

    @property
    @abstractmethod
    def input_model(self) -> type[BaseModel]:
        """Pydantic model that defines and validates the tool's input arguments."""

    @property
    def schema(self) -> dict:
        """JSON Schema derived from input_model, passed to the LLM as the tool spec."""
        return self.input_model.model_json_schema()

    @abstractmethod
    async def execute(self, **kwargs):
        """
        Run the tool with the given keyword arguments and return a result dict.

        Arguments are validated against input_model before execution.
        """
