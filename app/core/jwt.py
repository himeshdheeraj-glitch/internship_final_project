from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
import jwt
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.constants import JWT_SUBJECT_ACCESS, JWT_SUBJECT_REFRESH

def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an access token (JWT) containing subject (user ID) and role.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": subject,
        "role": role,
        "type": JWT_SUBJECT_ACCESS,
        "exp": int(expire.timestamp())
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a refresh token (JWT) containing subject (user ID).
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {
        "sub": subject,
        "type": JWT_SUBJECT_REFRESH,
        "exp": int(expire.timestamp())
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str, is_refresh: bool = False) -> Dict:
    """
    Decodes and validates a JWT access or refresh token.
    Raises UnauthorizedException if invalid/expired.
    """
    secret = settings.JWT_REFRESH_SECRET_KEY if is_refresh else settings.JWT_SECRET_KEY
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[settings.JWT_ALGORITHM]
        )
        # Check type
        expected_type = JWT_SUBJECT_REFRESH if is_refresh else JWT_SUBJECT_ACCESS
        if payload.get("type") != expected_type:
            raise UnauthorizedException(message="Invalid token type")
            
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(message="Token signature has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException(message="Invalid token signature")
