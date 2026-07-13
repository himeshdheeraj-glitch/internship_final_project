import uuid
from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.jwt import decode_token
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(message="Token payload is missing subject")
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException(message="Invalid user identifier inside token")
        
    query = select(User).where(User.id == user_uuid, User.deleted_at == None).options(
        selectinload(User.role)
    )
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise UnauthorizedException(message="User matching credentials does not exist")
    if not user.is_active:
        raise UnauthorizedException(message="User account is deactivated")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UnauthorizedException(message="Inactive user account")
    return current_user
