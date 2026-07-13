import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException, BadRequestException
from app.core.logging import logger
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.models.users import User
from app.repositories.users import user_repository
from app.repositories.auth import auth_repository
from app.schemas.auth import UserRegister, TokenResponse

class AuthService:
    async def register_user(self, db: AsyncSession, *, user_in: UserRegister) -> User:
        logger.info(f"Attempting registration for email: {user_in.email}")
        existing_user = await user_repository.get_by_email(db, str(user_in.email))
        if existing_user:
            raise ConflictException(message="A user with this email address already exists")

        role_name = (user_in.role_name or "buyer").lower().strip()
        role = await user_repository.get_role_by_name(db, role_name)
        if not role:
            raise BadRequestException(message="Specified role is invalid or does not exist")
            
        hashed_password = hash_password(user_in.password)
        user_dict = {
            "email": str(user_in.email).strip().lower(),
            "hashed_password": hashed_password,
            "first_name": user_in.first_name,
            "last_name": user_in.last_name,
            "phone_number": user_in.phone_number,
            "role_id": role.id,
            "is_active": True,
            "is_verified": False
        }
        user = await user_repository.create(db, obj_in=user_dict)

        await auth_repository.create_audit_log(
            db, user_id=user.id, action="register", table_name="users", record_id=user.id
        )
        return await user_repository.get_user_with_role(db, user.id)

    async def authenticate_user(
        self, db: AsyncSession, *, email: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None
    ) -> Tuple[User, TokenResponse]:
        logger.info(f"Authentication attempt for email: {email}")
        user = await user_repository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(message="Incorrect email or password")
            
        if not user.is_active:
            raise UnauthorizedException(message="Inactive account")
            
        await auth_repository.revoke_refresh_tokens(db, user.id)
        
        access_token = create_access_token(subject=str(user.id), role=user.role.name)
        refresh_token_jwt = create_refresh_token(subject=str(user.id))
        
        expiry_dt = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        await auth_repository.create_refresh_token(db, user_id=user.id, token=refresh_token_jwt, expires_at=expiry_dt)
        
        await auth_repository.create_audit_log(
            db, user_id=user.id, action="login", table_name="users", record_id=user.id, ip_address=ip_address, user_agent=user_agent
        )
        return user, TokenResponse(access_token=access_token, refresh_token=refresh_token_jwt)

    async def refresh_access_token(self, db: AsyncSession, *, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token, is_refresh=True)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedException(message="Invalid token structure")
            
        db_token = await auth_repository.get_refresh_token(db, refresh_token)
        if not db_token or db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise UnauthorizedException(message="Expired or revoked refresh token")
            
        user = db_token.user
        if not user.is_active:
            raise UnauthorizedException(message="User account is deactivated")
            
        await auth_repository.revoke_refresh_tokens(db, user.id)
        
        new_access_token = create_access_token(subject=str(user.id), role=user.role.name)
        new_refresh_token = create_refresh_token(subject=str(user.id))
        
        expiry_dt = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        await auth_repository.create_refresh_token(db, user_id=user.id, token=new_refresh_token, expires_at=expiry_dt)
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def logout_user(self, db: AsyncSession, *, user_id: uuid.UUID) -> None:
        await auth_repository.revoke_refresh_tokens(db, user_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="logout", table_name="users", record_id=user_id)

auth_service = AuthService()
