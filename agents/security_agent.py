from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import SecurityReport
import os
import json

def run_security_agent(pr_diff: str) -> SecurityReport:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    language = os.getenv("LANGUAGE", "en")

    system_prompt = f"""You are a security code reviewer.
Analyze the given PR diff and identify security vulnerabilities.
Scan based on OWASP Top 10: hardcoded passwords/API keys, SQL injection, XSS, unsafe imports.
Only report issues you actually see in the code. Do not fabricate findings.

IMPORTANT: Respond ONLY in {language} language. Every single word in your response must be in {language}.
Return a JSON object in this exact format, no other text:
{{
  "findings": [
    {{
      "issue": "issue description in {language}",
      "severity": 8,
      "line": 3,
      "suggestion": "suggestion in {language}"
    }}
  ],
  "summary": "summary in {language}"
}}"""

    human_prompt = f"""Analyze the following PR diff for security issues:

{pr_diff}"""

    result = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])

    # Parse JSON manually
    text = result.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    data = json.loads(text)
    return SecurityReport(**data)