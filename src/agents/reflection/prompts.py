def reflection_prompt(research_content: str) -> str:
    return f"""You are a reflection agent.

Critically review the following research.

Identify:
- missing information
- weak reasoning
- unsupported claims
- possible hallucinations

Research:

{research_content}
"""
