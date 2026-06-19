def fact_check_prompt(research: str, reflection: str) -> str:
    return f"""You are a fact-checking agent.

Verify the accuracy of the following research.

Check for:
- factual inaccuracies
- unsupported statements
- contradictions

Research:

{research}

Reflection:

{reflection}
"""
