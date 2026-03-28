from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import TestReport
import os

def run_test_agent(pr_diff: str) -> TestReport:
    """
    Analyzes PR diff for missing test coverage.
    Returns a structured TestReport including suggested test code.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(TestReport)
    language = os.getenv("LANGUAGE", "en")
    system_prompt = f"""You are a test coverage reviewer.
Analyze the given PR diff and identify missing tests.
Look for: new functions without tests, uncovered edge cases,
missing error handling tests.
Also write the actual pytest test code for the missing cases in suggested_tests field. Respond in {language} language."""

    human_prompt = f"""Analyze the following PR diff for missing test coverage: Respond in {language} language.

{pr_diff}"""

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result