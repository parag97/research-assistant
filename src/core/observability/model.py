from datetime import datetime
from pydantic import BaseModel, Field

class TraceEvent(BaseModel):

    workflow_id: str 
    node_name: str
    start_time: datetime
    end_time: datetime
    duration_ms: float 



