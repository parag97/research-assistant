from functools import cached_property
from core.llm.factory import get_llm
from core.runtime.agent_runtime import AgentRuntime

from agents.research.agent import ResearchAgent
from agents.reflection.agent import ReflectionAgent
from agents.evaluation.agent import EvaluationAgent
from agents.fact_check.agent import FactCheckAgent



class Container:

    @cached_property
    def llm(self):
        return get_llm()


    @cached_property
    def runtime(self):

        return AgentRuntime(
            llm=self.llm,
        )
    @cached_property
    def research_agent(self):
        return ResearchAgent(
            self.runtime
        )

    @cached_property
    def reflection_agent(self):
        return ReflectionAgent(
            self.runtime
        )

    @cached_property
    def evaluation_agent(self):
        return EvaluationAgent(
            self.runtime
        )

    @cached_property
    def fact_check_agent(self):
        return FactCheckAgent(
            self.runtime
        )