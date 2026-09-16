from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models.models import (
    User,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Explainable AI-Powered Intelligent Color Formulation & Optimization Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API. Access API docs at /docs."
    }
