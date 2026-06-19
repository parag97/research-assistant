from abc import ABC
from abc import abstractmethod


class BaseWorkflow(ABC):

    @abstractmethod
    def build(self):
        pass