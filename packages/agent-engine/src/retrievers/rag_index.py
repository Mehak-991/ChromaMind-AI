import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict, Any


class RAGIndexBuilder:
    def __init__(self, index_dir: str = "./vector_db/faiss_index"):
        self.index_dir = index_dir
        # Enforce local CPU execution of sentence-transformers embedding
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_index(self, docs: List[Dict[str, Any]]):
        langchain_docs = []
        for d in docs:
            langchain_docs.append(
                Document(
                    page_content=d["content"],
                    metadata={
                        "title": d.get("title", "Untitled"),
                        "category": d.get("category", "General"),
                        "source": d.get("source", "System KB"),
                    },
                )
            )

        db = FAISS.from_documents(langchain_docs, self.embeddings)
        os.makedirs(os.path.dirname(self.index_dir), exist_ok=True)
        db.save_local(self.index_dir)
        return db

    def load_retriever(self):
        if os.path.exists(self.index_dir):
            db = FAISS.load_local(
                self.index_dir, self.embeddings, allow_dangerous_deserialization=True
            )
            return db.as_retriever(search_kwargs={"k": 3})

        # Fallback in memory DB if local store is empty
        fallback_doc = Document(
            page_content="Lightness increases when white pigments are added, reducing mixed color saturation.",
            metadata={"title": "Basic Mixing", "category": "Mixing"},
        )
        db = FAISS.from_documents([fallback_doc], self.embeddings)
        return db.as_retriever(search_kwargs={"k": 2})
