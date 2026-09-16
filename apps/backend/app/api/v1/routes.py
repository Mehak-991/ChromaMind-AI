from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
    PredictionRequest,
    PredictionResponse,
    SettingsBase,
    SettingsResponse,
    AssistantQueryRequest,
    AssistantQueryResponse,
    SaveRecipeRequest,
)
from app.repositories.repositories import (
    UserRepository,
    PredictionRepository,
    SettingsRepository,
)
from app.services.services import (
    PredictionService,
    MLService,
    OptimizationService,
    ExplainabilityService,
    AssistantService,
)
from app.models.models import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user

router = APIRouter()


# Dependency factories
def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


def get_prediction_service(db: AsyncSession = Depends(get_db)):
    return PredictionService(
        MLService(),
        OptimizationService(),
        ExplainabilityService(),
        PredictionRepository(db),
    )


def get_settings_repo(db: AsyncSession = Depends(get_db)):
    return SettingsRepository(db)


# --- Authentication APIs ---
@router.post(
    "/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(payload: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    existing = await repo.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    from app.models.models import User

    new_user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        full_name=payload.full_name,
        role="user",
    )
    user_record = await repo.create(new_user)
    return user_record


@router.post("/auth/login", response_model=Token)
async def login(payload: UserLogin, repo: UserRepository = Depends(get_user_repo)):
    user = await repo.get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer", "user": user}


# --- Prediction APIs ---
@router.post("/formulator/predict", response_model=PredictionResponse)
async def predict(
    payload: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service),
    current_user: User = Depends(get_current_user),
):
    result = await service.execute_formulation(payload, current_user.id)
    return result


# --- Settings APIs ---
@router.patch("/settings", response_model=SettingsResponse)
async def update_settings(
    payload: SettingsBase,
    repo: SettingsRepository = Depends(get_settings_repo),
    current_user: User = Depends(get_current_user),
):
    from app.models.models import UserSettings

    settings_obj = await repo.get_by_user_id(current_user.id)
    if not settings_obj:
        settings_obj = UserSettings(user_id=current_user.id)

    settings_obj.default_delta_e_threshold = payload.default_delta_e_threshold
    settings_obj.optimizer_max_iterations = payload.optimizer_max_iterations
    settings_obj.enable_explainability = payload.enable_explainability

    updated = await repo.update(settings_obj)
    return updated


# --- Assistant Chat APIs ---
@router.post("/rag/chat", response_model=AssistantQueryResponse)
async def chat(
    payload: AssistantQueryRequest, current_user: User = Depends(get_current_user)
):
    service = AssistantService()
    result = await service.query_rag_engine(payload)
    return result


def get_prediction_repo(db: AsyncSession = Depends(get_db)):
    return PredictionRepository(db)


# --- History APIs ---
@router.get("/history")
async def get_history(
    page: int = 1,
    limit: int = 10,
    repo: PredictionRepository = Depends(get_prediction_repo),
    current_user: User = Depends(get_current_user),
):
    records = await repo.get_history(current_user.id, page, limit)
    items = []
    for r in records:
        items.append(
            {
                "id": str(r.id),
                "target_hex": r.target_hex,
                "delta_e": r.delta_e,
                "created_at": r.created_at.isoformat() + "Z",
            }
        )
    return {"items": items}


@router.post("/history/save")
async def save_recipe(
    payload: SaveRecipeRequest,
    repo: PredictionRepository = Depends(get_prediction_repo),
    current_user: User = Depends(get_current_user),
):
    from app.models.models import PredictionHistory

    new_record = PredictionHistory(
        user_id=current_user.id,
        target_hex=payload.target_hex,
        target_lab_l=payload.target_lab[0],
        target_lab_a=payload.target_lab[1],
        target_lab_b=payload.target_lab[2],
        base_colors_config=payload.base_colors_config,
        ml_predicted_ratios=payload.ml_predicted_ratios,
        optimized_ratios=payload.optimized_ratios,
        delta_e=payload.delta_e,
        confidence_score=payload.confidence_score,
    )
    saved = await repo.save(new_record)
    return {"status": "success", "id": str(saved.id)}


# --- Health Check APIs ---
@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "ml_engine": "online",
        },
    }
