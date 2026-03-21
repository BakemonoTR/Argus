from pydantic import BaseModel
from typing import List
import os
import hashlib

# --- Shared finding structure for all agents ---

class SecurityFinding(BaseModel):
    issue: str
    severity: int        # 1-10
    line: int
    suggestion: str

class SecurityReport(BaseModel):
    findings: List[SecurityFinding]
    summary: str

# --- Performance ---

class PerformanceFinding(BaseModel):
    issue: str
    severity: int
    line: int
    suggestion: str

class PerformanceReport(BaseModel):
    findings: List[PerformanceFinding]
    summary: str

# --- Style ---

class StyleFinding(BaseModel):
    issue: str
    severity: int
    line: int
    suggestion: str

class StyleReport(BaseModel):
    findings: List[StyleFinding]
    summary: str

# --- Test Coverage ---

class TestFinding(BaseModel):
    missing_test: str
    severity: int
    suggestion: str

class TestReport(BaseModel):
    findings: List[TestFinding]
    summary: str
    
    # --- Debate ---

class Conflict(BaseModel):
    issue: str                  # What the conflict is about
    agent_a: str                # First agent's name
    severity_a: int             # First agent's severity score
    agent_b: str                # Second agent's name
    severity_b: int             # Second agent's severity score
    final_severity: int         # Debate agent's final decision
    reasoning: str              # Why this score was chosen

class FinalReport(BaseModel):
    conflicts: List[Conflict]   # All detected conflicts and resolutions
    critical_issues: List[str]  # Issues with final severity >= 8
    should_autofix: bool        # True if any critical issue exists
    overall_summary: str        # One paragraph executive summary

API_KEY = os.environ.get('API_KEY')
PASSWORD = hashlib.sha256(os.environ.get('PASSWORD').encode()).hexdigest()

def get_report(agent_name: str) -> FinalReport:
    # Using parameterized query to prevent SQL injection
    query = "SELECT * FROM reports WHERE agent_name = %s"
    params = (agent_name,)
    # Execute the query with the given parameters
    # This is a mock example, actual implementation may vary based on the database library being used
    report = execute_query(query, params)
    return report

def execute_query(query: str, params: tuple) -> FinalReport:
    # This is a mock example, actual implementation may vary based on the database library being used
    # For example, using psycopg2 library for PostgreSQL database
    import psycopg2
    conn = psycopg2.connect(
        dbname="database",
        user="username",
        password=PASSWORD,
        host="host",
        port="port"
    )
    cur = conn.cursor()
    cur.execute(query, params)
    report = cur.fetchone()
    conn.close()
    return report