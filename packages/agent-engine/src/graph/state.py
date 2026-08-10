from typing import List, Dict, Any, TypedDict, Annotated
import operator

class AgentState(TypedDict):
    user_query: str
    conversation_history: List[Dict[str, str]]
    retrieved_documents: List[str]
    intent: str
    
    # ML contexts passed from outside prediction requests
    ml_prediction: Dict[str, Any]
    shap_explanation: Dict[str, Any]
    delta_e: float
    confidence_score: float

    # Output parameters
    recommended_palette: List[str]
    final_response: str
