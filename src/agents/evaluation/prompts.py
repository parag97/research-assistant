def evaluation_prompt(research: str, reflection: str) -> str:
    return f"""You are an evaluation agent.

Assess the quality of the research and decide whether it is ready or needs revision.

Research:
{research}

Reflection:
{reflection}
"""
