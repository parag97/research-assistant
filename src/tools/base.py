from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass


    @property
    @abstractmethod
    def description(self) -> str:
        pass


    @property
    @abstractmethod
    def input_model(self) -> type[BaseModel]:
        pass


    @property
    def schema(self):

        return (
            self.input_model
            .model_json_schema()
        )


    @abstractmethod
    async def execute(
        self,
        **kwargs,
    ):
        pass