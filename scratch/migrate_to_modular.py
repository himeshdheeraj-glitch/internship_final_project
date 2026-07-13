import os
import shutil

def run_migration():
    # 1. Create target directories if they don't exist
    dirs = [
        "app/core", "app/database", "app/shared", "app/auth", "app/users",
        "app/properties", "app/reviews", "app/favorites", "app/amenities",
        "app/locations", "app/notifications", "app/analytics", "app/admin"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "__init__.py"), "w") as f:
            pass

    # Helper function to write file and log
    def write_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {path}")

    # ==================== app/core/config.py ====================
    config_content = """import json
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
    ] = ["http://localhost:3000", "http://localhost:8000"]

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
"""
    write_file("app/core/config.py", config_content)

    # ==================== app/database/base.py ====================
    db_base_content = """import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

class Base(DeclarativeBase):
    metadata = metadata

class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )
"""
    write_file("app/database/base.py", db_base_content)

    # ==================== app/database/session.py ====================
    db_session_content = """from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
"""
    write_file("app/database/session.py", db_session_content)

    # ==================== app/shared/responses.py ====================
    shared_resp_content = """from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Request completed successfully"
    data: Optional[T] = None
"""
    write_file("app/shared/responses.py", shared_resp_content)

    # ==================== app/shared/pagination.py ====================
    shared_pag_content = """import math
from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number, starting from 1"),
        size: int = Query(default=20, ge=1, le=100, description="Items per page")
    ) -> None:
        self.page = page
        self.size = size

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "Page[T]":
        pages = math.ceil(total / params.size) if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
"""
    write_file("app/shared/pagination.py", shared_pag_content)

    # ==================== app/shared/validators.py ====================
    shared_val_content = """import re
from typing import Optional

def validate_phone_format(phone: Optional[str]) -> bool:
    if not phone:
        return True
    pattern = r"^\+?[1-9]\d{1,14}$"
    return bool(re.match(pattern, phone))

def validate_zip_format(zip_code: str) -> bool:
    pattern = r"^[a-zA-Z0-9\s\-]{3,10}$"
    return bool(re.match(pattern, zip_code))
"""
    write_file("app/shared/validators.py", shared_val_content)

    # ==================== app/shared/helpers.py ====================
    shared_help_content = """import random
import string
import re

def generate_random_token(length: int = 32) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.SystemRandom().choice(chars) for _ in range(length))

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")
"""
    write_file("app/shared/helpers.py", shared_help_content)

    # ==================== app/shared/image_utils.py ====================
    shared_img_content = """from app.core.logging import logger

def optimize_image_dimensions(width: int, height: int, max_size: int = 1920) -> tuple[int, int]:
    if width <= max_size and height <= max_size:
        return width, height
    if width > height:
        ratio = max_size / width
        return max_size, int(height * ratio)
    else:
        ratio = max_size / height
        return int(width * ratio), max_size

def watermark_image(image_path: str) -> None:
    logger.info(f"Watermarking image file at: {image_path}")
"""
    write_file("app/shared/image_utils.py", shared_img_content)

    # ==================== app/shared/email.py ====================
    shared_email_content = """from app.core.logging import logger

async def send_email(email_to: str, subject: str, body: str) -> None:
    logger.info("--- MOCK EMAIL DISPATCH ---")
    logger.info(f"To: {email_to}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Body: {body}")
    logger.info(f"---------------------------")

async def send_verification_email(email_to: str, token: str) -> None:
    await send_email(email_to, "Verify your email address", f"Verification token: {token}")

async def send_reset_password_email(email_to: str, token: str) -> None:
    await send_email(email_to, "Reset your password", f"Reset link token: {token}")
"""
    write_file("app/shared/email.py", shared_email_content)

    # ==================== app/shared/file_upload.py ====================
    shared_upload_content = """import os
import uuid
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import BadRequestException
from app.core.logging import logger

async def save_uploaded_file(file: UploadFile, folder: str) -> str:
    filename = file.filename or "file"
    ext = filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise BadRequestException(message=f"File extension '.{ext}' is not allowed")
        
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise BadRequestException(message="File size exceeds limit")
    await file.seek(0)
    
    target_dir = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(target_dir, exist_ok=True)
    
    unique_filename = f"{uuid.uuid4()}.{ext}"
    dest_path = os.path.join(target_dir, unique_filename)
    
    with open(dest_path, "wb") as f:
        f.write(content)
        
    return f"/static/uploads/{folder}/{unique_filename}"
"""
    write_file("app/shared/file_upload.py", shared_upload_content)

    print("Common shared layers migrated.")

if __name__ == "__main__":
    run_migration()
