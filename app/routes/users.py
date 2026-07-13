from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.users import UserResponse, UserUpdate, ChangePasswordRequest
from app.services.users import user_service
from app.shared.file_upload import save_uploaded_file

router = APIRouter(prefix="/users", tags=["Users Profile"])

@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    return APIResponse(message="Profile retrieved", data=current_user)

@router.put("/me", response_model=APIResponse[UserResponse])
async def update_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await user_service.update_profile(db, user_id=current_user.id, user_update=user_update)
    return APIResponse(message="Profile updated", data=user)

@router.post("/me/change-password", response_model=APIResponse[None])
async def change_password(req: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await user_service.change_password(db, user_id=current_user.id, old_password=req.old_password, new_password=req.new_password)
    return APIResponse(message="Password changed successfully")

@router.post("/me/profile-image", response_model=APIResponse[UserResponse])
async def upload_profile_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    image_url = await save_uploaded_file(file, folder="profile_images")
    user = await user_service.update_profile(db, user_id=current_user.id, user_update=UserUpdate(profile_image_url=image_url))
    return APIResponse(message="Image uploaded successfully", data=user)
