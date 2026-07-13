from typing import Dict, Any, List
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.properties import Property
from app.models.reviews import Review
from app.models.locations import City
from app.repositories.users import user_repository
from app.repositories.properties import property_repository
from app.repositories.reviews import review_repository

class AnalyticsService:
    async def get_dashboard_stats(self, db: AsyncSession) -> Dict[str, Any]:
        total_users = await user_repository.count_users(db)
        total_properties = await property_repository.count_properties_total(db)
        total_reviews = await review_repository.count_reviews_total(db)

        most_viewed_query = (
            select(Property)
            .where(Property.deleted_at == None, Property.status == "published")
            .order_by(desc(Property.views_count))
            .limit(5)
        )
        res_viewed = await db.execute(most_viewed_query)
        most_viewed = list(res_viewed.scalars().all())

        popular_cities_query = (
            select(City.name, func.count(Property.id).label("property_count"))
            .join(Property, Property.city_id == City.id)
            .where(Property.deleted_at == None)
            .group_by(City.name)
            .order_by(desc("property_count"))
            .limit(5)
        )
        res_cities = await db.execute(popular_cities_query)
        popular_cities = [{"city": row[0], "count": row[1]} for row in res_cities.all()]

        return {
            "totals": {
                "users": total_users,
                "properties": total_properties,
                "reviews": total_reviews
            },
            "most_viewed_properties": [
                {
                    "id": str(p.id),
                    "title": p.title,
                    "price": float(p.price),
                    "views": p.views_count
                }
                for p in most_viewed
            ],
            "popular_cities": popular_cities
        }

analytics_service = AnalyticsService()
