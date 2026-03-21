from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os

def run_autofix_agent(original_code: str, critical_issues: list) -> str:
    """
    Takes the original code and critical issues,
    returns fixed version of the code.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    issues_text = "\n".join(f"- {issue}" for issue in critical_issues)

    system_prompt = """You are a senior software engineer.
You will be given code with critical security and performance issues.
Fix ONLY the critical issues listed. Do not refactor or change anything else.
Return ONLY the fixed code, no explanations, no markdown code blocks."""

    human_prompt = f"""Fix the following critical issues in this code:

CRITICAL ISSUES TO FIX:
{issues_text}

ORIGINAL CODE:
{original_code}"""

    result = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result.content