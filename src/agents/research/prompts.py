from langsmith.schemas import Feedback
def research_prompt(query: str, feedback: str = "") -> str:
    base = f"""You are a research agent.

    Research the following topic thoroughly:

    {query}




    """
    if feedback != "":
            base += f"""
    Improve your research using this feedback from a previous attempt:

    {feedback}
    """

    base += """
    Provide:
    - facts
    - explanations
    - context
    """

    return base
