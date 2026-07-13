from __future__ import annotations
import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
if TYPE_CHECKING:
    from app.models.properties import Property
    
class Country(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)

    states: Mapped[List["State"]] = relationship("State", back_populates="country", cascade="all, delete-orphan")

class State(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "states"

    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False
    )

    country: Mapped["Country"] = relationship("Country", back_populates="states")
    cities: Mapped[List["City"]] = relationship("City", back_populates="state", cascade="all, delete-orphan")

class City(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    state_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("states.id", ondelete="CASCADE"), nullable=False
    )

    state: Mapped["State"] = relationship("State", back_populates="cities")
    properties: Mapped[List["Property"]] = relationship("Property", back_populates="city")
