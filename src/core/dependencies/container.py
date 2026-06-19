from functools import cached_property
from core.llm.factory import get_llm


class Container:

    @cached_property
    def llm(self):
        return get_llm()
