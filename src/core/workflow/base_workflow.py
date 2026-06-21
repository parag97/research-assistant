from abc import ABC, abstractmethod


class BaseWorkflow(ABC):
    """
    Abstract base class for all LangGraph workflow implementations.

    Subclasses must implement build(), which assembles and compiles
    a StateGraph and returns the runnable graph object.
    """

    @abstractmethod
    def build(self):
        """
        Assemble the workflow graph and return a compiled runnable.

        Returns
        -------
        A compiled LangGraph graph that can be invoked via .invoke()
        or .ainvoke().
        """
