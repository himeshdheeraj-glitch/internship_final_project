from __future__ import annotations
import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin
if TYPE_CHECKING:
    from app.models.locations import City
    from app.models.users import User
    from app.models.amenities import PropertyAmenity
    from app.models.favorites import Favorite
    from app.models.reviews import Review
    
class PropertyType(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "property_types"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    properties: Mapped[List["Property"]] = relationship("Property", back_populates="property_type")

class Property(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "properties"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), index=True, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cities.id", ondelete="RESTRICT"), nullable=False
    )
    property_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_types.id", ondelete="RESTRICT"), nullable=False
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    purpose: Mapped[Optional[str]] = mapped_column(String(50), default="For Sale", nullable=True)
    parking: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
    furnishing_status: Mapped[Optional[str]] = mapped_column(String(50), default="Unfurnished", nullable=True)
    agent_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    agent_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    agent_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    city: Mapped["City"] = relationship("City", back_populates="properties")
    property_type: Mapped["PropertyType"] = relationship("PropertyType", back_populates="properties")
    owner: Mapped["User"] = relationship("User", back_populates="properties")
    images: Mapped[List["PropertyImage"]] = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    property_amenities: Mapped[List["PropertyAmenity"]] = relationship("PropertyAmenity", back_populates="property", cascade="all, delete-orphan")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="property", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="property", cascade="all, delete-orphan")

class PropertyImage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "property_images"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    property: Mapped["Property"] = relationship("Property", back_populates="images")
