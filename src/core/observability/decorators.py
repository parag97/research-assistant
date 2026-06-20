from langgraph.store.base import Result
from datetime import UTC, datetime
from functools import wraps
from core.observability.model import TraceEvent

def tracer_node(node_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, state):
            start_time = datetime.now(UTC)
            result = await func(self, state)

            end_time = datetime.now(UTC)
            self.agent.runtime.observability.record(
                    TraceEvent(
                        workflow_id="workflow",
                        node_name=node_name,
                        start_time=start_time,
                        end_time=end_time,
                        duration_ms=(
                            end_time - start_time
                        ).total_seconds()
                        * 1000,
                    )
                )

            return result

        return wrapper
    return decorator
