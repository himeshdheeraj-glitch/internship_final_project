import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.permissions import RoleChecker
from app.core.constants import UserRole
from app.models.users import User
from app.schemas.users import UserResponse, UserUpdateRole
from app.schemas.properties import PropertyResponse
from app.services.users import user_service
from app.services.properties import property_service
from app.services.analytics import analytics_service

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/users", response_model=APIResponse[List[UserResponse]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def list_platform_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    users = await user_service.list_users(db, skip=skip, limit=limit)
    return APIResponse(message="Users list retrieved", data=users)

@router.put("/users/{user_id}/role", response_model=APIResponse[UserResponse])
async def change_user_role(
    user_id: uuid.UUID, role_update: UserUpdateRole, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)
):
    user = await user_service.update_user_role(db, user_id=user_id, role_name=role_update.role_name, admin_id=current_admin.id)
    return APIResponse(message="User role updated successfully", data=user)

@router.post("/users/{user_id}/deactivate", response_model=APIResponse[None])
async def deactivate_user(user_id: uuid.UUID, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    await user_service.deactivate_user(db, user_id=user_id, admin_id=current_admin.id)
    return APIResponse(message="User deactivated successfully")

@router.delete("/users/{user_id}", response_model=APIResponse[None])
async def delete_user(user_id: uuid.UUID, current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)):
    await user_service.delete_user(db, user_id=user_id, admin_id=current_admin.id)
    return APIResponse(message="User deleted successfully")

@router.get("/properties", response_model=APIResponse[Page[PropertyResponse]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def admin_list_properties(params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    pages = await property_service.list_properties(db, status=None, params=params)
    return APIResponse(message="Admin listings retrieved", data=pages)

@router.put("/properties/{property_id}/status", response_model=APIResponse[PropertyResponse])
async def change_property_status(
    property_id: uuid.UUID, status_val: str = Query(...), current_admin: User = Depends(RoleChecker([UserRole.ADMIN])), db: AsyncSession = Depends(get_db)
):
    from app.schemas.properties import PropertyUpdate
    update_schema = PropertyUpdate(status=status_val)
    prop = await property_service.update_property(db, property_id=property_id, property_update=update_schema, user_id=current_admin.id, is_admin=True)
    return APIResponse(message="Property status updated successfully", data=prop)

@router.get("/analytics/dashboard", response_model=APIResponse[Dict[str, Any]], dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db)):
    metrics = await analytics_service.get_dashboard_stats(db)
    return APIResponse(message="Metrics retrieved successfully", data=metrics)
