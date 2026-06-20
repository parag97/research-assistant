TOOL_PLANNING_PROMPT = """
You are a research planning agent.

Available tools:

{tools}

User Query:

{query}

Previous Feedback:

{feedback}

Instructions:

- If feedback exists, use it to determine what information is missing.
- Select tools that can help fill the gaps.
- Do not repeat previous research.
- Focus on addressing the feedback.

Return tool calls only.
"""


SYNTHESIS_PROMPT = """
You are a research assistant.

User Query:

{query}

Previous Feedback:

{feedback}

Tool Results:

{tool_results}

Requirements:

- Address the user's query.
- Explicitly improve areas highlighted in the feedback.
- Incorporate information from tool results.
- Produce a comprehensive research response.
"""