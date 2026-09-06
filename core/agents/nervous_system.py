from typing import TypedDict, Annotated, Sequence
import operator
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    # Dummy classes for when the network blocks pip install
    class StateGraph:
        def __init__(self, state_schema): pass
        def add_node(self, name, action): pass
        def set_entry_point(self, name): pass
        def add_edge(self, source, target): pass
        def compile(self): return self
    END = "END"


# Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    current_plan: str
    execution_result: str
    review_status: str
    decision: str

# Dummy Nodes
def planner_node(state: AgentState):
    print("--- PLANNER ---")
    return {"current_plan": "Dummy plan generated."}

def executor_node(state: AgentState):
    print("--- EXECUTOR ---")
    return {"execution_result": "Dummy execution completed."}

def reviewer_node(state: AgentState):
    print("--- REVIEWER ---")
    return {"review_status": "Dummy review passed."}

def memory_node(state: AgentState):
    print("--- MEMORY ---")
    return {"messages": ["Stored dummy memory."]}

def decision_node(state: AgentState):
    print("--- DECISION ---")
    return {"decision": "Proceed to END."}

def build_nervous_system():
    """Builds the agent graph."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("memory", memory_node)
    workflow.add_node("decision", decision_node)

    # Add edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "reviewer")
    workflow.add_edge("reviewer", "memory")
    workflow.add_edge("memory", "decision")
    workflow.add_edge("decision", END)

    # Compile
    app = workflow.compile()
    return app

if __name__ == "__main__":
    app = build_nervous_system()
    print("Agent Nervous System initialized.")
    # Run a dummy input to verify it compiles and runs
    # app.invoke({"messages": ["Start task"]})
