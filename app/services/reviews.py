import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.shared.pagination import Page, PaginationParams
from app.models.reviews import Review
from app.repositories.reviews import review_repository
from app.repositories.properties import property_repository
from app.repositories.auth import auth_repository
from app.schemas.reviews import ReviewCreate, ReviewUpdate

class ReviewService:
    async def add_review(self, db: AsyncSession, *, review_in: ReviewCreate, user_id: uuid.UUID) -> Review:
        prop = await property_repository.get(db, review_in.property_id)
        if not prop or prop.deleted_at is not None:
            raise NotFoundException(message="Property not found")
        if prop.owner_id == user_id:
            raise BadRequestException(message="You cannot write reviews for your own property listings")
            
        review_dict = review_in.model_dump()
        review_dict["user_id"] = user_id
        review = await review_repository.create(db, obj_in=review_dict)
        await auth_repository.create_audit_log(db, user_id=user_id, action="create_review", table_name="reviews", record_id=review.id)
        return review

    async def update_review(
        self, db: AsyncSession, *, review_id: uuid.UUID, review_update: ReviewUpdate, user_id: uuid.UUID, is_admin: bool = False
    ) -> Review:
        rev = await review_repository.get(db, review_id)
        if not rev or rev.deleted_at is not None:
            raise NotFoundException(message="Review not found")
        if not is_admin and rev.user_id != user_id:
            raise ForbiddenException(message="You do not have permission to update this review")
            
        update_data = review_update.model_dump(exclude_unset=True)
        await review_repository.update(db, db_obj=rev, obj_in=update_data)
        await auth_repository.create_audit_log(db, user_id=user_id, action="update_review", table_name="reviews", record_id=review_id, new_values=update_data)
        return rev

    async def delete_review(self, db: AsyncSession, *, review_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> None:
        rev = await review_repository.get(db, review_id)
        if not rev or rev.deleted_at is not None:
            raise NotFoundException(message="Review not found")
        if not is_admin and rev.user_id != user_id:
            raise ForbiddenException(message="You do not have permission to delete this review")
        await review_repository.soft_delete(db, id=review_id)
        await auth_repository.create_audit_log(db, user_id=user_id, action="delete_review", table_name="reviews", record_id=review_id)

    async def get_property_reviews(self, db: AsyncSession, *, property_id: uuid.UUID, params: PaginationParams) -> Page:
        skip = (params.page - 1) * params.size
        items = await review_repository.get_property_reviews(db, property_id=property_id, skip=skip, limit=params.size)
        total = await review_repository.count_reviews_by_property(db, property_id=property_id)
        return Page.create(items=items, total=total, params=params)

    async def get_property_average_rating(self, db: AsyncSession, *, property_id: uuid.UUID) -> float:
        return await review_repository.get_property_average_rating(db, property_id)

review_service = ReviewService()
