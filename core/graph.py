from langgraph.graph import StateGraph, START, END
from core.state import PipelineState
from agents.security_agent import run_security_agent
from agents.performance_agent import run_performance_agent
from agents.style_agent import run_style_agent
from agents.test_agent import run_test_agent
from agents.debate_agent import run_debate_agent

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
    """
    Runs after all 4 agents are done.
    Reads their findings from state, produces final report.
    """
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

def build_graph():
    graph = StateGraph(PipelineState)

    # Register nodes
    graph.add_node("security_agent", security_node)
    graph.add_node("performance_agent", performance_node)
    graph.add_node("style_agent", style_node)
    graph.add_node("test_agent", test_node)
    graph.add_node("debate_agent", debate_node)

    # 4 agents run in parallel from START
    graph.add_edge(START, "security_agent")
    graph.add_edge(START, "performance_agent")
    graph.add_edge(START, "style_agent")
    graph.add_edge(START, "test_agent")

    # All 4 agents must finish before debate_agent runs
    graph.add_edge("security_agent", "debate_agent")
    graph.add_edge("performance_agent", "debate_agent")
    graph.add_edge("style_agent", "debate_agent")
    graph.add_edge("test_agent", "debate_agent")

    graph.add_edge("debate_agent", END)

    return graph.compile()