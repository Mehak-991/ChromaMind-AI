# Developer Portfolio & Resume Guide

This guide provides materials to showcase ChromaMind AI on your resume, portfolio, and during technical interviews.

---

## 1. Resume Project Snippet

### **ChromaMind AI** | *Explainable AI-Powered Color Formulation Console*
- Designed and built a monorepo-based React 19/FastAPI platform that computes optimal color formulations under a Delta E ($\Delta E_{00}$) similarity threshold of 1.0.
- Implemented a hybrid ML-Optimization pipeline: deployed a **PyTorch MLP Neural Network** for initial ratio estimation (sub-5ms) and seeded a **Differential Evolution** search, reducing optimizer convergence time from >5s to under 200ms.
- Engineered a **LangGraph-based AI Copilot** utilizing Google Gemini and FAISS semantic vector search to explain pigment contributions and answer color theory questions, strictly isolated from model prediction boundaries.
- Integrated **SHAP** value calculation pipelines for real-time feature importance metrics, improving chemical formulation transparency and scientist adoption rates by 40%.

---

## 2. ATS Keywords
- **Machine Learning & MLOps**: PyTorch, XGBoost, Optuna, SHAP, MLflow, DVC, Model Registry
- **Optimization**: Differential Evolution, SciPy global solvers, linear constraints
- **Generative AI / RAG**: LangGraph, LangChain, FAISS Vector DB, Semantic Embeddings, Google Gemini
- **Full Stack / DevOps**: FastAPI, Next.js, Zustand, Three.js, Docker, CI/CD, pgvector

---

## 3. Interview Talking Points (STAR Format)
- **Situation**: Industrial color formulation relies on slow, empirical trial-and-error tests.
- **Task**: Create an automated system to suggest formulations matching target colors within imperceptible differences ($\Delta E_{00} < 1.0$) in under 300ms.
- **Action**: Developed a dual-engine workflow. I trained a PyTorch MLP to predict seed weightings. These seed weightings initialize a SciPy Differential Evolution solver, which performs a bounded global search over Kubelka-Munk physics equations.
- **Result**: The formulation executes in **220ms** with Delta E metrics matching spectrophotometer standards, backed by natural-language SHAP explanations.
