from langgraph.graph import StateGraph, START, END
from core.state import PipelineState
from agents.security_agent import run_security_agent

def security_node(state: PipelineState) -> PipelineState:
    """
    Reads pr_diff from state, runs security agent,
    writes findings back into state.
    """
    report = run_security_agent(state["pr_diff"])

    # Convert Pydantic objects to dicts so state can store them
    findings = [finding.model_dump() for finding in report.findings]

    return {
        "security_findings": findings,
        "summary": report.summary
    }

def build_graph():
    graph = StateGraph(PipelineState)

    # Register our node
    graph.add_node("security_agent", security_node)

    # Define the flow: START → security_agent → END
    graph.add_edge(START, "security_agent")
    graph.add_edge("security_agent", END)

    return graph.compile()