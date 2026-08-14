import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "ChromaMind AI"
    API_V1_STR: str = "/api/v1"
    
    # Security configs
    JWT_SECRET: str = Field(default="super_secret_jwt_sign_key_902183", env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # DB Connections
    DATABASE_URL: str = Field(
        default="postgresql://admin:SecretPassword123@localhost:5432/chromamind_db",
        env="DATABASE_URL"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Third-Party Integrations
    ML_SERVICE_URL: str = Field(default="http://localhost:8500", env="ML_SERVICE_URL")
    LLM_SERVICE_URL: str = Field(default="http://localhost:8600", env="LLM_SERVICE_URL")
    VECTOR_DB_URL: str = Field(default="http://localhost:6333", env="VECTOR_DB_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
