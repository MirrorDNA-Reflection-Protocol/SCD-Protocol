"""
LangGraph + SCD Protocol Demo

This example shows how to use mirrordna-scd as a deterministic state layer
inside a simple LangGraph workflow.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, END
from mirrordna_scd import SCDProtocol


# Define the agent state structure LangGraph will pass around
class AgentState(TypedDict, total=False):
    input: str
    analysis: str
    scd_context: str


# Initialize the SCD state engine
# Using an on-disk file makes state reusable across runs; set to None for in-memory only.
scd = SCDProtocol(state_file="agent_state.json")


def analyze(state: AgentState) -> AgentState:
    """
    Simple LangGraph node that:
    - updates SCD deterministic state with the latest input
    - returns a human-readable SCD context string
    """

    user_input = state.get("input", "")

    # Update deterministic state
    scd.supersede(
        {
            "user_input": user_input,
            "last_node": "analyze",
        }
    )

    # Build SCD-backed context string
    ctx = scd.get_context_string()

    return {
        "analysis": f"Received input: {user_input!r}. Deterministic state updated.",
        "scd_context": ctx,
    }


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("analyze", analyze)
    graph.set_entry_point("analyze")
    graph.set_finish_point("analyze")

    return graph.compile()


if __name__ == "__main__":
    print("Running LangGraph + SCD demo...\n")

    # Build the graph
    app = build_graph()

    # Invoke with a sample input
    initial_state: AgentState = {"input": "Hello from MirrorDNA and SCD!"}
    result = app.invoke(initial_state)

    print("LangGraph result:")
    print(result)
    print()

    # Show SCD internals
    print("SCD deterministic state:")
    print(scd.get_state())
    print()

    print("SCD checksum:")
    print(scd.get_checksum())
    print()

    print("SCD context string:")
    print(scd.get_context_string())
    print()

    print("Done.")
