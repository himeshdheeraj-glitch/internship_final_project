import json
from typing import List
from pydantic import BeforeValidator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    APP_NAME: str = "Real Estate API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # JWT Security Settings
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "real_estate"
    DATABASE_URL: str

    # pgAdmin Settings
    PGADMIN_DEFAULT_EMAIL: str = "admin@realestate.com"
    PGADMIN_DEFAULT_PASSWORD: str = "admin"

    # CORS Settings
    CORS_ORIGINS: Annotated[
        List[str],
        BeforeValidator(lambda v: json.loads(v) if isinstance(v, str) else v)
    ] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # Image Upload Settings
    UPLOAD_DIR: str = "app/uploads"
    MAX_FILE_SIZE: int = 5242880  # 5MB
    ALLOWED_IMAGE_EXTENSIONS: Annotated[
        List[str],
        BeforeValidator(lambda v: json.loads(v) if isinstance(v, str) else v)
    ] = ["jpg", "jpeg", "png", "webp"]

    # Initial Admin Settings
    INIT_ADMIN_EMAIL: str = "admin@realestate.com"
    INIT_ADMIN_PASSWORD: str = "AdminPassword123!"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, info) -> str:
        if isinstance(v, str) and v:
            return v
        
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        host = info.data.get("POSTGRES_HOST")
        port = info.data.get("POSTGRES_PORT")
        db = info.data.get("POSTGRES_DB")
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

settings = Settings()
