from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional, Any
from uuid import UUID
from datetime import datetime


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional['UserResponse'] = None


class TokenPayload(BaseModel):
    sub: str
    exp: int
    role: str


# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Login Schema ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Settings Schemas ---
class SettingsBase(BaseModel):
    default_delta_e_threshold: float = Field(1.0, ge=0.1, le=10.0)
    optimizer_max_iterations: int = Field(1000, ge=100, le=10000)
    enable_explainability: bool = True


class SettingsResponse(SettingsBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


# --- Color Formulation Schemas ---
class LabColor(BaseModel):
    L: float = Field(..., ge=0.0, le=100.0)
    a: float = Field(..., ge=-128.0, le=128.0)
    b: float = Field(..., ge=-128.0, le=128.0)


class BaseColorInput(BaseModel):
    id: str
    hex: str = Field(..., min_length=4, max_length=7)
    lab: LabColor
    name: Optional[str] = None


class TargetColorInput(BaseModel):
    hex: str = Field(..., min_length=4, max_length=7)
    lab: LabColor


class PredictionRequest(BaseModel):
    target_color: TargetColorInput
    base_colors: List[BaseColorInput]
    run_optimization: bool = True

    @field_validator("base_colors")
    def validate_bases_count(cls, v):
        if len(v) < 3 or len(v) > 8:
            raise ValueError("Must provide between 3 and 8 base colors.")
        return v


class BaseRatio(BaseModel):
    id: str
    ratio: float
    weight_grams: float


class PredictionResponse(BaseModel):
    prediction_id: UUID
    target_color: TargetColorInput
    formulation: Dict[str, Any]
    explanation: Dict[str, Any]


# --- Assistant Schemas ---
class AssistantQueryRequest(BaseModel):
    message: str = Field(..., min_length=1)
    prediction_context_id: Optional[UUID] = None


class AssistantQueryResponse(BaseModel):
    response: str
    citations: List[Dict[str, Any]]


class SaveRecipeRequest(BaseModel):
    target_hex: str
    target_lab: List[float]
    base_colors_config: List[Dict[str, Any]]
    ml_predicted_ratios: List[float]
    optimized_ratios: List[float]
    delta_e: float
    confidence_score: float
