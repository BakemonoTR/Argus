from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import FinalReport
import json
import os

def run_debate_agent(
    security_findings: list,
    performance_findings: list,
    style_findings: list,
    test_findings: list
) -> FinalReport:
    """
    Reviews all agent findings, resolves conflicts,
    and produces a final consolidated report.
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(FinalReport)
    language = os.getenv("LANGUAGE", "en")
    system_prompt = f"""You are a senior engineering lead acting as a debate judge.
You receive findings from 4 specialized code review agents.
Your job:
1. Identify conflicts — same issue reported by multiple agents with different severity scores (difference >= 3)
2. For each conflict, reason about the correct final severity and explain why
3. List all critical issues (final severity >= 8)
4. Decide if the PR needs an automatic fix (should_autofix = true if any critical issue exists)
5. Write a concise overall summary for the PR author

Be fair and precise. If two agents disagree, consider both perspectives. Respond in {language} language."""

    # Build a structured input so the agent can see all findings clearly
    all_findings = {
        "security_agent": security_findings,
        "performance_agent": performance_findings,
        "style_agent": style_findings,
        "test_agent": test_findings
    }

    human_prompt = f"""Review the following findings from all agents and produce a final report:
    
{json.dumps(all_findings, indent=2)}
"""

    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    return result