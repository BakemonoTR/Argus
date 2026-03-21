from langgraph.graph import StateGraph, START, END
from core.state import PipelineState
from agents.security_agent import run_security_agent
from agents.performance_agent import run_performance_agent
from agents.style_agent import run_style_agent
from agents.test_agent import run_test_agent
from agents.debate_agent import run_debate_agent
from agents.autofix_agent import run_autofix_agent
from core.github_client import get_file_content, create_autofix_branch
import os
import secrets

def security_node(state: PipelineState) -> dict:
    report = run_security_agent(state["pr_diff"])
    return {
        "security_findings": [f.model_dump() for f in report.findings],
        "security_summary": report.summary
    }

def performance_node(state: PipelineState) -> dict:
    report = run_performance_agent(state["pr_diff"])
    return {
        "performance_findings": [f.model_dump() for f in report.findings],
        "performance_summary": report.summary
    }

def style_node(state: PipelineState) -> dict:
    report = run_style_agent(state["pr_diff"])
    return {
        "style_findings": [f.model_dump() for f in report.findings],
        "style_summary": report.summary
    }

def test_node(state: PipelineState) -> dict:
    report = run_test_agent(state["pr_diff"])
    return {
        "test_findings": [f.model_dump() for f in report.findings],
        "test_summary": report.summary
    }

def debate_node(state: PipelineState) -> dict:
    report = run_debate_agent(
        security_findings=state["security_findings"],
        performance_findings=state["performance_findings"],
        style_findings=state["style_findings"],
        test_findings=state["test_findings"]
    )
    return {
        "conflicts": [c.model_dump() for c in report.conflicts],
        "critical_issues": report.critical_issues,
        "should_autofix": report.should_autofix,
        "overall_summary": report.overall_summary
    }

def autofix_node(state: PipelineState) -> dict:
    """
    Runs only if should_autofix is True.
    Fetches changed files, fixes critical issues, creates a new branch.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise Exception("API key not set")
    
    repo_name = os.getenv("REPO_NAME")
    pr_number = int(os.getenv("PR_NUMBER", "1"))
    source_branch = os.getenv("SOURCE_BRANCH", "test-pr-branch")
    password = os.getenv("PASSWORD")
    if not password:
        raise Exception("Password not set")

    fixed_files = {}

    for file_path in state["files_changed"]:
        # Only fix Python files
        if not file_path.endswith(".py"):
            continue
        try:
            original_code = get_file_content(repo_name, file_path, source_branch)
            fixed_code = run_autofix_agent(original_code, state["critical_issues"])
            fixed_files[file_path] = fixed_code
        except Exception as e:
            print(f"Could not fix {file_path}: {e}")

    if fixed_files:
        branch_name = create_autofix_branch(
            repo_name=repo_name,
            pr_number=pr_number,
            source_branch=source_branch,
            fixed_files=fixed_files
        )
        print(f"Auto-fix branch created: {branch_name}")

    return {}  # No state update needed

def should_run_autofix(state: PipelineState) -> str:
    """
    Conditional edge: run autofix only if should_autofix is True.
    """
    if state.get("should_autofix"):
        return "autofix_agent"
    return END

def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("security_agent", security_node)
    graph.add_node("performance_agent", performance_node)
    graph.add_node("style_agent", style_node)
    graph.add_node("test_agent", test_node)
    graph.add_node("debate_agent", debate_node)
    graph.add_node("autofix_agent", autofix_node)

    # 4 agents run in parallel
    graph.add_edge(START, "security_agent")
    graph.add_edge(START, "performance_agent")
    graph.add_edge(START, "style_agent")
    graph.add_edge(START, "test_agent")

    # All feed into debate
    graph.add_edge("security_agent", "debate_agent")
    graph.add_edge("performance_agent", "debate_agent")
    graph.add_edge("style_agent", "debate_agent")
    graph.add_edge("test_agent", "debate_agent")

    # Conditional: autofix only if needed
    graph.add_conditional_edges("debate_agent", should_run_autofix)
    graph.add_edge("autofix_agent", END)

    return graph.compile()