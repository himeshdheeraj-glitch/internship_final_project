from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.schemas.users import UserResponse
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, user_in=user_in)
    return APIResponse(message="User registered successfully", data=user)

@router.post("/login", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def login(request: Request, credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    _, tokens = await auth_service.authenticate_user(db, email=credentials.email, password=credentials.password, ip_address=ip_address, user_agent=user_agent)
    return APIResponse(message="Authentication successful", data=tokens)

@router.post("/refresh", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def refresh(refresh_in: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    tokens = await auth_service.refresh_access_token(db, refresh_token=refresh_in.refresh_token)
    return APIResponse(message="Access token refreshed", data=tokens)

@router.post("/logout", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await auth_service.logout_user(db, user_id=current_user.id)
    return APIResponse(message="User logged out successfully")

@router.post("/forgot-password", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def forgot_password(req: ForgotPasswordRequest):
    return APIResponse(message="Password reset link sent")

@router.post("/reset-password", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def reset_password(req: ResetPasswordRequest):
    return APIResponse(message="Password reset successfully")
