import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.shared.responses import APIResponse
from app.shared.pagination import Page, PaginationParams
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.reviews import review_service

router = APIRouter(tags=["Reviews"])

@router.get("/properties/{property_id}/reviews", response_model=APIResponse[Page[ReviewResponse]])
async def get_reviews(property_id: uuid.UUID, params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    pages = await review_service.get_property_reviews(db, property_id=property_id, params=params)
    return APIResponse(message="Reviews list retrieved", data=pages)

@router.post("/reviews", response_model=APIResponse[ReviewResponse], status_code=status.HTTP_201_CREATED)
async def create_review(review_in: ReviewCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rev = await review_service.add_review(db, review_in=review_in, user_id=current_user.id)
    return APIResponse(message="Review submitted successfully", data=rev)

@router.put("/reviews/{review_id}", response_model=APIResponse[ReviewResponse])
async def update_review(review_id: uuid.UUID, review_update: ReviewUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    rev = await review_service.update_review(db, review_id=review_id, review_update=review_update, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Review updated successfully", data=rev)

@router.delete("/reviews/{review_id}", response_model=APIResponse[None])
async def delete_review(review_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_admin = current_user.role.name == "admin"
    await review_service.delete_review(db, review_id=review_id, user_id=current_user.id, is_admin=is_admin)
    return APIResponse(message="Review deleted successfully")
