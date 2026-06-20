from core.observability.model import TraceEvent

class WorkflowTracer:

    def __init__(self):
        self.events : list[TraceEvent] = []

    def record(self, event: TraceEvent):
        self.events.append(event)
    
    def clear(self):
        self.events.clear()

    def dump(self):
        return self.events.copy()

