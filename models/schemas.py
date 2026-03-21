from pydantic import BaseModel
from typing import List

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
    missing_test: str        # What is not tested
    severity: int
    suggestion: str          # What test should be written

class TestReport(BaseModel):
    findings: List[TestFinding]
    suggested_tests: str     # Actual test code as a string
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