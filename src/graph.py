from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents import (
    orchestrator_node,
    booking_node,
    logistics_node,
    marketing_node,
    weather_node,
    evaluator_node
)
from src.config import langfuse_handler

workflow = StateGraph(AgentState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("booking", booking_node)
workflow.add_node("logistics", logistics_node)
workflow.add_node("marketing", marketing_node)
workflow.add_node("weather", weather_node) 
workflow.add_node("evaluator", evaluator_node) 

workflow.set_entry_point("orchestrator")

workflow.add_conditional_edges(
    "orchestrator",
    lambda state: state["next_node"],
    {
        "booking": "booking",
        "logistics": "logistics",
        "marketing": "marketing",
        "weather": "weather"    
    }
)

workflow.add_edge("booking", "evaluator")
workflow.add_edge("logistics", "evaluator")
workflow.add_edge("marketing", "evaluator")
workflow.add_edge("weather", "evaluator")

workflow.add_edge("evaluator", END)

app = workflow.compile()
print("✅ Grafo de TourMaster compilado correctamente")

def run_tourmaster_graph(query: str):
    """
    Función helper para invocar el grafo desde main.py o los tests.
    """
    inputs = {"query": query}
    
    config = {
        "configurable": {"thread_id": "1"},
        "callbacks": [langfuse_handler] 
    }
    
    result = app.invoke(inputs, config=config)
    return result