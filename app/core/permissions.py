from typing import List
from fastapi import Depends
from app.core.exceptions import ForbiddenException
from app.models.users import User
from app.core.constants import UserRole
from app.core.dependencies import get_current_user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]) -> None:
        self.allowed_roles = [role.value if isinstance(role, UserRole) else role for role in allowed_roles]

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        # Resolve role name from relation
        if current_user.role.name not in self.allowed_roles:
            raise ForbiddenException(
                message=f"Access denied. Required roles: {self.allowed_roles}. Current role: {current_user.role.name}"
            )
        return current_user
