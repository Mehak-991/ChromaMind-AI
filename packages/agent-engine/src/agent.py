from src.graph.workflow import create_agent_graph
from typing import Dict, Any, List


class ChromaMindAgent:
    def __init__(self):
        self.graph = create_agent_graph()

    async def invoke_agent(
        self,
        query: str,
        ml_prediction: Dict[str, Any] = None,
        history: List[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        initial_state = {
            "user_query": query,
            "conversation_history": history or [],
            "retrieved_documents": [],
            "intent": "general",
            "ml_prediction": ml_prediction or {},
            "shap_explanation": {},
            "delta_e": 0.0,
            "confidence_score": 1.0,
            "recommended_palette": [],
            "final_response": "",
        }

        # Execute LangGraph compile context
        result = await self.graph.ainvoke(initial_state)

        return {
            "response": result["final_response"],
            "recommended_palette": result["recommended_palette"],
            "intent": result["intent"],
        }
