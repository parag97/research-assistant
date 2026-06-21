from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the research pipeline.

    Each agent is responsible for a single stage of the workflow
    (research, reflection, evaluation, fact-check, final evaluation).
    Agents receive an AgentRuntime and any required config values at
    construction — they never read config themselves.
    """

    @abstractmethod
    async def run(self, *args, **kwargs):
        """
        Execute the agent's task and return its output artifact.

        All agents are async to allow concurrent LLM and tool calls.
        """
