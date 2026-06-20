def final_evaluation_prompt(
    research: str,
    reflection: str,
    fact_check: str,
) -> str:
    return f"""You are a senior research reviewer.

Your job is to perform the FINAL quality assessment of a research report.

The report has already gone through:
1. Research generation
2. Reflection and critique
3. Fact checking

You are NOT deciding whether to revise the report.
You are evaluating the overall quality of the final result that would be delivered to a user.

Evaluate using these criteria:
- Accuracy
- Completeness
- Clarity
- Internal consistency
- Usefulness
- Trustworthiness

Research Report:
----------------
{research}

Reflection:
-----------
{reflection}

Fact Check:
-----------
{fact_check}

Return:
- score: value between 0.0 and 1.0
- summary: concise overall assessment
- strengths: list of major strengths
- weaknesses: list of remaining weaknesses
- ready_for_delivery: true if the report is suitable for end users
"""
