# Prompt for ReflectionAgent.
# Expects {research_content} via .format() — called in reflection_prompt().


def reflection_prompt(research_content: str) -> str:
    """Build the reflection prompt for the given research content."""

    return f"""You are a reflection agent.

Your job is to critically review the research below and identify weaknesses.

Identify:
- Missing or incomplete information
- Weak or unsupported reasoning
- Unsupported claims that need citations or evidence
- Possible hallucinations or factual errors

Research:

{research_content}

Be specific and constructive. Your feedback will be used to improve the research
in the next iteration.
"""
