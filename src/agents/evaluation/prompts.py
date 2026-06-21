# Prompt for EvaluationAgent.
# Returns a structured EvaluationResult — the model must produce valid JSON
# matching the schema. Called in evaluation_prompt().


def evaluation_prompt(research: str, reflection: str) -> str:
    """Build the evaluation prompt for the given research and reflection."""

    return f"""You are an evaluation agent.

Your job is to assess the quality of the research and decide whether it is
ready to proceed, or needs another revision pass.

Research:
{research}

Reflection:
{reflection}

Evaluate the research on:
- Completeness: does it fully answer the query?
- Accuracy: are the claims supported and plausible?
- Clarity: is it well-structured and easy to understand?

Return a structured decision:
- approved: true if the research is ready, false if it needs revision
- score: a quality score between 0.0 and 1.0
- decision: "approve" or "revise"
- feedback: a brief explanation of your decision
- issues: a list of specific problems (if decision is "revise")
"""
