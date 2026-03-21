from typing import TypedDict, List

class PipelineState(TypedDict):
    pr_diff: str
    files_changed: List[str]          # ← yeni eklendi

    security_findings: List[dict]
    performance_findings: List[dict]
    style_findings: List[dict]
    test_findings: List[dict]

    security_summary: str
    performance_summary: str
    style_summary: str
    test_summary: str

    conflicts: List[dict]
    critical_issues: List[str]
    should_autofix: bool
    overall_summary: str