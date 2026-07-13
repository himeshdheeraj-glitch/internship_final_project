import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema
from app.schemas.users import UserResponse
from app.schemas.locations import CityResponse

class PropertyTypeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class PropertyTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class PropertyTypeResponse(BaseResponseSchema):
    name: str
    description: Optional[str] = None

class PropertyImageCreate(BaseModel):
    property_id: uuid.UUID
    url: str = Field(..., max_length=500)
    is_cover: bool = False
    display_order: int = 0

class PropertyImageResponse(BaseResponseSchema):
    property_id: uuid.UUID
    url: str
    is_cover: bool
    display_order: int

class AmenityResponse(BaseResponseSchema):
    name: str
    description: Optional[str] = None

class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=2000)
    price: float = Field(..., ge=0)
    bedrooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    area: float = Field(..., ge=0)
    address: str = Field(..., min_length=5, max_length=255)
    zip_code: str = Field(..., min_length=2, max_length=20)
    city_id: uuid.UUID
    property_type_id: uuid.UUID
    status: Optional[str] = "draft"
    is_featured: Optional[bool] = False
    amenity_ids: Optional[List[uuid.UUID]] = Field(default_factory=list)
    purpose: Optional[str] = "For Sale"
    parking: Optional[bool] = False
    furnishing_status: Optional[str] = "Unfurnished"
    agent_name: Optional[str] = Field(None, max_length=100)
    agent_phone: Optional[str] = Field(None, max_length=20)
    agent_email: Optional[str] = Field(None, max_length=255)

class PropertyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    price: Optional[float] = Field(None, ge=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    area: Optional[float] = Field(None, ge=0)
    address: Optional[str] = Field(None, min_length=5, max_length=255)
    zip_code: Optional[str] = Field(None, min_length=2, max_length=20)
    city_id: Optional[uuid.UUID] = None
    property_type_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None
    amenity_ids: Optional[List[uuid.UUID]] = None
    purpose: Optional[str] = None
    parking: Optional[bool] = None
    furnishing_status: Optional[str] = None
    agent_name: Optional[str] = Field(None, max_length=100)
    agent_phone: Optional[str] = Field(None, max_length=20)
    agent_email: Optional[str] = Field(None, max_length=255)

class PropertyResponse(BaseResponseSchema):
    title: str
    description: str
    price: float
    bedrooms: int
    bathrooms: int
    area: float
    address: str
    zip_code: str
    status: str
    is_featured: bool
    views_count: int
    city_id: uuid.UUID
    property_type_id: uuid.UUID
    owner_id: uuid.UUID
    purpose: Optional[str] = None
    parking: Optional[bool] = None
    furnishing_status: Optional[str] = None
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None
    agent_email: Optional[str] = None
    
    city: Optional[CityResponse] = None
    property_type: Optional[PropertyTypeResponse] = None
    owner: Optional[UserResponse] = None
    images: List[PropertyImageResponse] = Field(default_factory=list)
    amenities: List[AmenityResponse] = Field(default_factory=list)
