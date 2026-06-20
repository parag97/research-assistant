from pydantic import BaseModel


class ToolCall(
    BaseModel,
):
    tool_name: str

    arguments: dict


class ToolPlan(
    BaseModel,
):
    tool_calls: list[ToolCall]