from typing import TypedDict, List
import os
import sqlite3

class PipelineState(TypedDict):
    pr_diff: str
    files_changed: List[str]         
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

API_KEY = os.environ.get('API_KEY')
PASSWORD = os.environ.get('PASSWORD')

def query_database(query: str, params: tuple):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result