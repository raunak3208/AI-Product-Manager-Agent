import re
from langgraph.graph import StateGraph, END
from app.state import PMState
from app.agents.research_agent import run_research_agent
from app.agents.writing_agent import run_writing_agent
from app.agents.critic_agent import run_critic_agent

MAX_REVISIONS = 3

def research_node(state: PMState) -> dict:
    research = run_research_agent(state["idea"])
    return {"research": research}

def writing_node(state: PMState) -> dict:
    prd = run_writing_agent(state["research"], state["features"])
    return {"prd": prd}

def critic_node(state: PMState) -> dict:
    feedback = run_critic_agent(state["prd"])
    score = extract_score(feedback)
    revision_count = state.get("revision_count", 0) + 1
    return {
        "critic_feedback": feedback,
        "critic_score": score,
        "revision_count": revision_count,
    }

def extract_score(feedback: str) -> float:
    match = re.search(r"[Oo]verall.*?(\d\.\d+)", feedback)
    if match:
        return float(match.group(1))
    return 0.0

def should_revise(state: PMState) -> str:
    if state["critic_score"] >= 0.85:
        return "end"
    if state["revision_count"] >= MAX_REVISIONS:
        return "end"
    return "revise"

def build_graph():
    graph = StateGraph(PMState)

    graph.add_node("research", research_node)
    graph.add_node("write", writing_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "critic")

    graph.add_conditional_edges(
        "critic",
        should_revise,
        {"revise": "write", "end": END},
    )

    return graph.compile()