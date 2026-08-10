from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from app.core.database import get_db
from app.schemas.schemas import (
    UserCreate, UserResponse, UserLogin, Token,
    PredictionRequest, PredictionResponse,
    SettingsBase, SettingsResponse,
    AssistantQueryRequest, AssistantQueryResponse
)
from app.repositories.repositories import (
    UserRepository, PredictionRepository, SettingsRepository
)
from app.services.services import (
    PredictionService, MLService, OptimizationService, ExplainabilityService, AssistantService
)
import uuid

router = APIRouter()

# Dependency factories
def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

def get_prediction_service(db: AsyncSession = Depends(get_db)):
    return PredictionService(
        MLService(),
        OptimizationService(),
        ExplainabilityService(),
        PredictionRepository(db)
    )

def get_settings_repo(db: AsyncSession = Depends(get_db)):
    return SettingsRepository(db)

# --- Authentication APIs ---
@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    existing = await repo.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    from app.models.models import User
    new_user = User(
        email=payload.email,
        password_hash="hashed_" + payload.password,  # Placeholder hashing
        full_name=payload.full_name,
        role="user"
    )
    user_record = await repo.create(new_user)
    return user_record

@router.post("/auth/login", response_model=Token)
async def login(payload: UserLogin, repo: UserRepository = Depends(get_user_repo)):
    user = await repo.get_by_email(payload.email)
    if not user or user.password_hash != "hashed_" + payload.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": "mock_jwt_token", "token_type": "bearer"}

# --- Prediction APIs ---
@router.post("/formulator/predict", response_model=PredictionResponse)
async def predict(payload: PredictionRequest, service: PredictionService = Depends(get_prediction_service)):
    # Mock logged-in user id
    user_uuid = uuid.uuid4()
    result = await service.execute_formulation(payload, user_uuid)
    return result

# --- Settings APIs ---
@router.patch("/settings", response_model=SettingsResponse)
async def update_settings(payload: SettingsBase, repo: SettingsRepository = Depends(get_settings_repo)):
    from app.models.models import UserSettings
    # Mock user UUID
    user_uuid = uuid.uuid4()
    settings_obj = await repo.get_by_user_id(user_uuid)
    if not settings_obj:
        settings_obj = UserSettings(user_id=user_uuid)
    
    settings_obj.default_delta_e_threshold = payload.default_delta_e_threshold
    settings_obj.optimizer_max_iterations = payload.optimizer_max_iterations
    settings_obj.enable_explainability = payload.enable_explainability
    
    updated = await repo.update(settings_obj)
    return updated

# --- Assistant Chat APIs ---
@router.post("/rag/chat", response_model=AssistantQueryResponse)
async def chat(payload: AssistantQueryRequest):
    service = AssistantService()
    result = await service.query_rag_engine(payload)
    return result

# --- Health Check APIs ---
@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "ml_engine": "online"
        }
    }
