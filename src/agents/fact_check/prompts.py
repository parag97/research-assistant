# Prompt for FactCheckAgent.
# Called in fact_check_prompt() after the evaluation loop has approved
# the research and before final evaluation.


def fact_check_prompt(research: str, reflection: str) -> str:
    """Build the fact-check prompt for the given research and reflection."""

    return f"""You are a fact-checking agent.

Your job is to verify the accuracy of the research below.

Check for:
- Factual inaccuracies or incorrect statistics
- Unsupported statements presented as facts
- Internal contradictions within the research
- Claims that conflict with the reflection's critique

Research:

{research}

Reflection:

{reflection}

Be specific about any issues you find. If the research appears accurate,
state that clearly.
"""
