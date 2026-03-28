from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import StyleReport
import os

def run_style_agent(pr_diff: str) -> StyleReport:
    """
    Analyzes PR diff for code quality and style issues.
    Returns a structured StyleReport.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(StyleReport)
    language = os.getenv("LANGUAGE", "en")
    system_prompt = f"""You are a code quality reviewer.
Analyze the given PR diff and identify style and maintainability issues.
Look for: naming convention violations, dead code, functions that are too long,
missing docstrings, high complexity, magic numbers.
Only report issues you actually see. Do not fabricate findings. Respond in {language} language."""

    human_prompt = f"""Analyze the following PR diff for code style and quality issues: Respond in {language} language.

{pr_diff}"""

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result