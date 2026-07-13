import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logging import logger
from app.core.security import verify_password, hash_password
from app.models.users import User
from app.repositories.users import user_repository
from app.repositories.auth import auth_repository
from app.schemas.users import UserUpdate

class UserService:
    async def get_user_profile(self, db: AsyncSession, *, user_id: uuid.UUID) -> User:
        user = await user_repository.get_user_with_role(db, user_id)
        if not user:
            raise NotFoundException(message="User profile not found")
        return user

    async def update_profile(self, db: AsyncSession, *, user_id: uuid.UUID, user_update: UserUpdate) -> User:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        old_values = {"first_name": user.first_name, "last_name": user.last_name, "phone_number": user.phone_number, "profile_image_url": user.profile_image_url}
        await user_repository.update(db, db_obj=user, obj_in=user_update)
        new_values = user_update.model_dump(exclude_unset=True)
        
        await auth_repository.create_audit_log(
            db, user_id=user_id, action="update_profile", table_name="users", record_id=user_id, old_values=old_values, new_values=new_values
        )
        return await user_repository.get_user_with_role(db, user_id)

    async def change_password(self, db: AsyncSession, *, user_id: uuid.UUID, old_password: str, new_password: str) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        if not verify_password(old_password, user.hashed_password):
            raise BadRequestException(message="Incorrect old password")
        new_hashed = hash_password(new_password)
        await user_repository.update(db, db_obj=user, obj_in={"hashed_password": new_hashed})
        await auth_repository.create_audit_log(db, user_id=user_id, action="change_password", table_name="users", record_id=user_id)

    async def update_user_role(self, db: AsyncSession, *, user_id: uuid.UUID, role_name: str, admin_id: uuid.UUID) -> User:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        role = await user_repository.get_role_by_name(db, role_name)
        if not role:
            raise BadRequestException(message="Role not found")
            
        old_role_name = user.role.name if user.role else None
        await user_repository.update(db, db_obj=user, obj_in={"role_id": role.id})
        
        await auth_repository.create_audit_log(
            db, user_id=admin_id, action="update_user_role", table_name="users", record_id=user_id, old_values={"role": old_role_name}, new_values={"role": role_name}
        )
        return await user_repository.get_user_with_role(db, user_id)

    async def list_users(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        return await user_repository.get_users_list(db, skip=skip, limit=limit)

    async def deactivate_user(self, db: AsyncSession, *, user_id: uuid.UUID, admin_id: uuid.UUID) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        await user_repository.update(db, db_obj=user, obj_in={"is_active": False})
        await auth_repository.create_audit_log(db, user_id=admin_id, action="deactivate_user", table_name="users", record_id=user_id)

    async def delete_user(self, db: AsyncSession, *, user_id: uuid.UUID, admin_id: uuid.UUID) -> None:
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundException(message="User not found")
        await user_repository.soft_delete(db, id=user_id)
        await auth_repository.create_audit_log(db, user_id=admin_id, action="soft_delete_user", table_name="users", record_id=user_id)

user_service = UserService()
