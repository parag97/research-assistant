# Prompt for FinalEvaluationAgent.
# Run once at the end of the workflow after fact-checking. Produces a
# structured FinalEvaluationResult scored against delivery-readiness criteria.


def final_evaluation_prompt(research: str, reflection: str, fact_check: str) -> str:
    """Build the final evaluation prompt from all three pipeline outputs."""

    return f"""You are a senior research reviewer.

Your job is to perform the FINAL quality assessment of a completed research report.

The report has already gone through:
1. Research generation
2. Reflection and critique
3. Fact-checking

You are NOT deciding whether to revise the report — that stage is complete.
You are scoring the overall quality of the final deliverable as it would be
seen by an end user.

Evaluate using these criteria:
- Accuracy        : Are the facts correct and well-supported?
- Completeness    : Does it fully address the original query?
- Clarity         : Is it well-written and easy to understand?
- Consistency     : Are there any internal contradictions?
- Usefulness      : Would an end user find this valuable?
- Trustworthiness : Does it inspire confidence?

Research Report:
----------------
{research}

Reflection:
-----------
{reflection}

Fact Check:
-----------
{fact_check}

Return a structured assessment:
- score             : overall quality score between 0.0 and 1.0
- summary           : one concise paragraph summarising the assessment
- strengths         : list of the report's notable strengths
- weaknesses        : list of remaining gaps or issues
- ready_for_delivery: true if suitable for an end user, false otherwise
"""
