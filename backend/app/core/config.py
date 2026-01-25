# Pydantic settings to manage the environment variables.

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tunify"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "d191c23ed259918ba448041c6c83a5c4024e4e3c04d4b3d086f409ebf0c336fe"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://tunify_user:tunify_pass@db:5432/tunity_db"

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB

    # add the admin fields (optional)
    TUNIFY_ADMIN_EMAIL: Optional[str] = Field(None, env="TUNIFY_ADMIN_EMAIL")
    TUNIFY_ADMIN_PASSWORD: Optional[str] = Field(None, env="TUNIFY_ADMIN_PASSWORD")


    class Config:
        env_file = ".env"



settings = Settings()
