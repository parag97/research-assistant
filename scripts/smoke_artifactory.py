from textwrap import indent
from core.models.artifact import (
    ResearchArtifact,
    Source,
)

artifact = ResearchArtifact(
    content="OpenAI released a new model.",
    confidence=0.95,
    sources=[
        Source(
            title="Example Source",
            path="https://example.com",
            content="Model announcement",
        )
    ],
    metadata={
        "provider": "openai",
        "run_id": "123",
    },
)

print(artifact.model_dump())