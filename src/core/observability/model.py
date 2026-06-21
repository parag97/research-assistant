from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TraceEvent(BaseModel):
    """
    Immutable record of a single node execution within a workflow run.

    Emitted by the @tracer_node decorator and stored in WorkflowTracer.
    One TraceEvent is created per node call regardless of success or failure.

    Fields
    ------
    workflow_id : Identifier of the workflow run that produced this event.
    node_name   : Name of the node that was traced (e.g. "ResearchNode").
    start_time  : UTC timestamp when the node started executing.
    end_time    : UTC timestamp when the node finished (or failed).
    duration_ms : Wall-clock execution time in milliseconds.
    status      : "success" if the node completed normally, "failure" otherwise.
    error       : Exception type and message if status is "failure", else None.
    """

    workflow_id: str
    node_name: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    status: Literal["success", "failure"] = "success"
    error: str | None = None
