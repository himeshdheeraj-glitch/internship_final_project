from __future__ import annotations
import uuid
from typing import List, TYPE_CHECKING 

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, UUIDPrimaryKeyMixin, TimestampMixin

                                                                                                                                                                                                                                                                                

if TYPE_CHECKING:
    from app.models.properties import Property
class Amenity(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    property_amenities: Mapped[List["PropertyAmenity"]] = relationship("PropertyAmenity", back_populates="amenity", cascade="all, delete-orphan")

class PropertyAmenity(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "property_amenities"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    amenity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("property_id", "amenity_id", name="uq_property_amenities_property_amenity"),
    )

    property: Mapped["Property"] = relationship("Property", back_populates="property_amenities")
    amenity: Mapped["Amenity"] = relationship("Amenity", back_populates="property_amenities")
