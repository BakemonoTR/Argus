from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import PerformanceReport
import os

def run_performance_agent(pr_diff: str) -> PerformanceReport:
    """
    Analyzes PR diff for performance issues.
    Returns a structured PerformanceReport.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(PerformanceReport)
    language = os.getenv("LANGUAGE", "en")
    system_prompt = f"""You are a performance-focused code reviewer.
Analyze the given PR diff and identify performance issues.
Look for: O(n²) or worse loops, database queries inside loops (N+1 problem),
repeated expensive computations, unnecessary memory allocations.
Only report issues you actually see. Do not fabricate findings. Respond in {language} language."""

    human_prompt = f"""Analyze the following PR diff for performance issues:

{pr_diff}"""

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result