from pydantic import BaseModel


class ToolCall(BaseModel):
    """
    A single tool invocation requested by the LLM during planning.

    Fields
    ------
    tool_name : Name of the tool to call (must exist in ToolRegistry).
    arguments : Key-value pairs to pass to tool.execute().
    """

    tool_name: str
    arguments: dict


class ToolPlan(BaseModel):
    """
    The complete set of tool calls the LLM decided to make for a query.

    Returned by LLMProvider.invoke_with_tools() and
    LLMProvider.structured(..., schema=ToolPlan).
    An empty tool_calls list is valid and means the agent will synthesise
    research without any tool results.
    """

    tool_calls: list[ToolCall]
