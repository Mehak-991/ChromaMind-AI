# ChromaMind AI

> **An Explainable AI-Powered Intelligent Color Formulation & Optimization Platform**

ChromaMind AI is an enterprise-grade solution designed to predict and optimize color formulation ratios using user-selected base colors. It couples state-of-the-art Machine Learning models with global search optimization algorithms, Explainable AI (XAI), and Large Language Models (LLM) utilizing Retrieval-Augmented Generation (RAG) to provide scientifically accurate and explainable color recipes.

---

## 🌟 Key Features

- **Optimal Mixing Prediction**: Real-time ratio prediction using a custom deep neural network / XGBoost ensemble model.
- **Formulation Optimization**: Fine-tuning color ratios using **Differential Evolution** algorithms to minimize Delta E ($\Delta E_{00}$).
- **Explainable AI (XAI)**: SHAP-based feature importance visualization explaining why specific ratios are recommended.
- **RAG-Powered Copilot**: Context-aware assistant providing expert advice on color theory, mixing adjustments, and formulation physics.
- **Enterprise Dashboard**: Historical logging, batch analysis, user workspace state management, and real-time visualization.

---

## 🏗️ Core Architecture Overview

The system is organized as a monorepo adhering to clean architecture principles:

```
chromamind-ai/
├── apps/
│   ├── frontend/         # Next.js App Router (TypeScript, Tailwind, Zustand)
│   └── backend/          # FastAPI (Python 3.11, Pydantic, SQLAlchemy)
├── packages/
│   ├── ml-engine/        # Python ML pipelines, training, optimization & SHAP
│   └── shared-types/     # Common TypeScript & JSON schemas
├── docs/                 # Architectural specifications
└── docker-compose.yml    # Local development orchestrator
```

For a comprehensive deep dive into the architecture, please refer to:
- 📑 [System Architecture Blueprint](./architecture_blueprint.md)
- 🔌 [API Documentation](./docs/API.md)
- 🗄️ [Database Architecture](./docs/DATABASE.md)
- 🔬 [Machine Learning & Optimization](./docs/ML.md)
- 🐳 [Deployment Guide](./docs/DEPLOYMENT.md)
- 🤝 [Contributing Guidelines](./docs/CONTRIBUTING.md)

---

## 🛠️ Stack & Technologies

| Layer | Technologies |
|---|---|
| **Frontend** | React, Next.js (App Router), TypeScript, Tailwind CSS, Framer Motion, Zustand, Chart.js / Recharts |
| **Backend** | Python 3.11, FastAPI, Pydantic, SQLAlchemy, Celery (Redis broker), Uvicorn |
| **Database** | PostgreSQL (with `pgvector` for RAG and semantic logs) |
| **ML & Analytics** | PyTorch, XGBoost, Scikit-Learn, SHAP, SciPy (Differential Evolution), Pandas, NumPy |
| **LLM & RAG** | Gemini / OpenAI API, LangChain/LlamaIndex, SentenceTransformers |
| **Infrastructure** | Docker, GitHub Actions, Prometheus, Grafana, Nginx |

---

## 🚀 Quick Start (Development)

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Setup and Running locally
1. Clone the repository and navigate to the directory:
   ```bash
   git clone https://github.com/your-org/chromamind-ai.git
   cd chromamind-ai
   ```
2. Start the database dependencies via Docker Compose (requires Docker to be running):
   ```bash
   docker-compose up -d postgres redis
   ```
3. Copy the environment variables template and start the Backend:
   ```bash
   # Terminal 1
   cd apps/backend
   cp .env.example .env
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Start the Frontend in a separate terminal:
   ```bash
   # Terminal 2
   cd apps/frontend
   npm install
   npm run dev
   ```

**Backend Diagnostics:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 🔑 Environment Variables Specification

The system loads parameters from `.env` files in respective project roots.

| Variable Name | Purpose | Example / Default Value | Scope | Requirement |
|---|---|---|---|---|
| **`JWT_SECRET`** | Key to sign authentication JSON Web Tokens. | `YOUR_SECRET_KEY` | Backend | **Required** |
| **`DATABASE_URL`** | Connection string for PostgreSQL database. | `postgresql://admin:CHANGE_ME@localhost:5432/chromamind_db` | Backend | **Required** |
| **`REDIS_URL`** | Redis cache connection string. | `redis://localhost:6379/0` | Backend | **Required** |
| **`VITE_API_URL`** | React Axios base endpoint connection path. | `http://localhost:8000/api/v1` | Frontend | **Required** |
| **`GEMINI_API_KEY`** | Google Gemini Generative API key. | `YOUR_GEMINI_API_KEY` | AI Agent | **Required** |
| **`MLFLOW_TRACKING_URI`** | Model parameter tracking dashboard URL. | `http://localhost:5000` | ML Engine | **Required** |

---

## 🛡️ License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
