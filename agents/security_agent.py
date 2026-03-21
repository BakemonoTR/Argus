from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import SecurityReport
import os

def run_security_agent(pr_diff: str) -> SecurityReport:
    """
    Analyzes PR diff for security vulnerabilities.
    Returns a structured SecurityReport.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(SecurityReport)

    system_prompt = """You are a security code reviewer.
Analyze the given PR diff and identify security vulnerabilities.
Scan based on OWASP Top 10: hardcoded passwords/API keys, SQL injection, XSS, unsafe imports.
Only report issues you actually see in the code. Do not fabricate findings."""

    human_prompt = f"""Analyze the following PR diff for security issues:

{pr_diff}"""

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result