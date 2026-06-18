# ADR-001: System Architecture

Status: Approved
Date: 2026-06-18

## Goal

Build a production-grade research platform that combines:

- Deep Research
- Reflection
- Fact Checking
- Personalized Briefings
- Long-Term Memory
- Strong Observability

---

# Decision 1: Workflow-Centric Architecture

Approved:

```text
Workflow
    ↓
Agent Teams
    ↓
Tools
```

Rejected:

```text
Agent
 ↓
Agent
 ↓
Agent
```

Reason:
- Deterministic execution
- Better observability
- Easier testing
- Easier governance

---

# Decision 2: Hybrid Supervisor Model

## Platform Router

Responsibilities:
- Select workflow
- Route requests

Implementation:
- Deterministic router
- Optional LLM assistance

## Team Leads

Responsibilities:
- Task decomposition
- Worker coordination
- Tool selection

Implementation:
- LLM-powered

---

# Decision 3: Artifact-Based Communication

Approved:

```text
ResearchArtifact
      ↓
ReflectionArtifact
      ↓
FactCheckArtifact
      ↓
FinalReport
```

Benefits:
- Strong contracts
- Replayability
- Evaluation support
- Human review support

---

# Decision 4: Three-Layer Memory

## Workflow Memory

Technology:
- LangGraph Checkpointer

Purpose:
- Persistence
- Resume
- Interrupts

## Agent Memory

Technology:
- LangChain Memory

Purpose:
- Scratchpad
- Temporary context

## Long-Term Memory

Technology:
- PostgreSQL
- Qdrant

Purpose:
- User Profile
- Projects
- Research History
- Semantic Memory

---

# Decision 5: Technology Mapping

## Runtime
- Python 3.13
- uv

## API
- FastAPI
- Pydantic v2

## Workflow
- LangGraph

## Agents
- LangChain Core

## Research
- Tavily

## Storage
- PostgreSQL
- Qdrant
- Redis

## Scheduling
- APScheduler

## Observability
- Langfuse
- OpenTelemetry
- Prometheus
- Grafana

## Evaluation
- DeepEval

## Deployment
- Docker Compose

---

# Decision 6: Observability First

Every:
- Workflow Run
- Agent Run
- Tool Call
- LLM Call
- Memory Operation

Must be traceable.

---

# Decision 7: Approved Workflows

## Research

Memory Retrieval
→ Research Team
→ Reflection Team
→ Fact Check Team
→ Writer

## Daily Brief

Scheduler
→ Memory Retrieval
→ Research Team
→ Reflection Team
→ Fact Check Team
→ Writer

---

# Future Expansion

- SQL Agent
- Code Execution Agent
- Human Approval
- MCP Integration
- Knowledge Graph Domain
- Multi-Tenant Support
- Temporal
