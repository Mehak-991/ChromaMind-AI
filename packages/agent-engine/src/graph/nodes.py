import os
from src.graph.state import AgentState
from src.retrievers.rag_index import RAGIndexBuilder
from src.tools.color_tools import ColorAgentTools
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any

class AgentNodes:
    def __init__(self):
        # Initialize Gemini API client
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY", "AIzaSyD_ExampleKey12345")
        )
        self.retriever_builder = RAGIndexBuilder()

    async def classify_intent(self, state: AgentState) -> Dict[str, Any]:
        query = state["user_query"].lower()
        intent = "general"
        if "why" in query or "ratio" in query or "shap" in query or "prediction" in query:
            intent = "explain_ml"
        elif "palette" in query or "match" in query:
            intent = "palette_recommendation"
        return {"intent": intent}

    async def retrieve_context(self, state: AgentState) -> Dict[str, Any]:
        retriever = self.retriever_builder.load_retriever()
        docs = retriever.get_relevant_documents(state["user_query"])
        content_snippets = [d.page_content for d in docs]
        return {"retrieved_documents": content_snippets}

    async def generate_response(self, state: AgentState) -> Dict[str, Any]:
        intent = state.get("intent", "general")
        docs = state.get("retrieved_documents", [])
        ml_context = state.get("ml_prediction", {})
        
        # Build strict prompt enforcing RAG boundaries & target predictions isolation
        prompt = f"""You are ChromaMind AI Copilot. Use the context to answer the user query.
        
        CRITICAL RULES:
        1. Never predict color mixing ratios. Ratios must only be calculated by the ML model.
        2. If explanation of ratios is required, describe how the coordinates shift using the context.

        Context: {chr(10).join(docs)}
        User Query: {state['user_query']}
        """

        if intent == "explain_ml" and ml_context:
            prompt += f"\nML prediction coordinates context: {ml_context}"

        # Call LLM
        response = self.llm.invoke(prompt)
        
        # Simple rule-based palette recommendation append
        palette = []
        if intent == "palette_recommendation":
            palette = ColorAgentTools.generate_palette("#3a86c8")

        return {
            "final_response": response.content,
            "recommended_palette": palette
        }
