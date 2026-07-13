import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal
from app.core.jwt import decode_token
from app.models.users import User

class AuthStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Default state
        request.state.user = None
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token)
                user_id_str = payload.get("sub")
                if user_id_str:
                    user_uuid = uuid.UUID(user_id_str)
                    
                    # Query user in a localized session for middleware safety
                    async with AsyncSessionLocal() as session:
                        query = select(User).where(User.id == user_uuid, User.deleted_at == None).options(
                            selectinload(User.role)
                        )
                        result = await session.execute(query)
                        user = result.scalars().first()
                        if user and user.is_active:
                            request.state.user = user
            except Exception:
                # Middleware does not fail requests, leaving it to Route dependencies
                pass
                
        return await call_next(request)
