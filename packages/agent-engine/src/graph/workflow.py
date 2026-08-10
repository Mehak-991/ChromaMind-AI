from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.nodes import AgentNodes

def create_agent_graph():
    nodes = AgentNodes()
    
    # Initialize state graph
    workflow = StateGraph(AgentState)
    
    # Register Nodes
    workflow.add_node("classify_intent", nodes.classify_intent)
    workflow.add_node("retrieve_context", nodes.retrieve_context)
    workflow.add_node("generate_response", nodes.generate_response)
    
    # Set Entry Point
    workflow.set_entry_point("classify_intent")
    
    # Set Edges
    workflow.add_edge("classify_intent", "retrieve_context")
    workflow.add_edge("retrieve_context", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Compile graph
    app = workflow.compile()
    return app
