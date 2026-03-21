from typing import TypedDict, List

class PipelineState(TypedDict):
    pr_diff: str                      # Input: PR's changed code
    security_findings: List[dict]     # Output: security agent results
    summary: str                      # Output: final summary