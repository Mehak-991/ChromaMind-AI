from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models.models import User, UserSession, PredictionHistory, UserSettings, Feedback, Analytics, ApiLog

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Explainable AI-Powered Intelligent Color Formulation & Optimization Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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
        
    from sqlalchemy import select
    from app.core.database import AsyncSessionLocal
    import uuid
    async with AsyncSessionLocal() as session:
        default_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
        result = await session.execute(select(User).where(User.id == default_id))
        user_record = result.scalars().first()
        if not user_record:
            default_user = User(
                id=default_id,
                email="admin@chromamind.ai",
                password_hash="hashed_admin",
                full_name="Dr. Carter",
                role="scientist"
            )
            session.add(default_user)
            await session.commit()

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API. Access API docs at /docs."
    }

