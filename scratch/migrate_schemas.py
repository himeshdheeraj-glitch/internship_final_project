import os

def migrate_schemas():
    def write_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written: {path}")

    # ==================== app/shared/schemas.py ====================
    shared_schemas = """import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseResponseSchema(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
"""
    write_file("app/shared/schemas.py", shared_schemas)

    # ==================== app/auth/schemas.py ====================
    auth_schemas = """from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    role_name: str = Field("buyer", description="admin, agent, seller, buyer")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("role_name")
    @classmethod
    def validate_role(cls, v: str) -> str:
        v = v.lower()
        if v not in ["admin", "agent", "seller", "buyer"]:
            raise ValueError("Role must be one of admin, agent, seller, buyer")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v
"""
    write_file("app/auth/schemas.py", auth_schemas)

    # ==================== app/users/schemas.py ====================
    users_schemas = """import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from app.shared.schemas import BaseResponseSchema

class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseResponseSchema):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    profile_image_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    role: RoleResponse

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    profile_image_url: Optional[str] = Field(None, max_length=500)

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserUpdateRole(BaseModel):
    role_name: str

    @field_validator("role_name")
    @classmethod
    def validate_role(cls, v: str) -> str:
        v = v.lower()
        if v not in ["admin", "agent", "seller", "buyer"]:
            raise ValueError("Role must be one of admin, agent, seller, buyer")
        return v
"""
    write_file("app/users/schemas.py", users_schemas)

    # ==================== app/locations/schemas.py ====================
    locations_schemas = """import uuid
from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema

class CountryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=2, max_length=10)

class CountryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=2, max_length=10)

class CountryResponse(BaseResponseSchema):
    name: str
    code: str

class StateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country_id: uuid.UUID

class StateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country_id: Optional[uuid.UUID] = None

class StateResponse(BaseResponseSchema):
    name: str
    country_id: uuid.UUID
    country: Optional[CountryResponse] = None

class CityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    state_id: uuid.UUID

class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    state_id: Optional[uuid.UUID] = None

class CityResponse(BaseResponseSchema):
    name: str
    state_id: uuid.UUID
    state: Optional[StateResponse] = None
"""
    write_file("app/locations/schemas.py", locations_schemas)

    # ==================== app/properties/schemas.py ====================
    properties_schemas = """import uuid
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
    
    city: Optional[CityResponse] = None
    property_type: Optional[PropertyTypeResponse] = None
    owner: Optional[UserResponse] = None
    images: List[PropertyImageResponse] = Field(default_factory=list)
    amenities: List[AmenityResponse] = Field(default_factory=list)
"""
    write_file("app/properties/schemas.py", properties_schemas)

    # ==================== app/amenities/schemas.py ====================
    amenities_schemas = """from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema

class AmenityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class AmenityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class AmenityResponse(BaseResponseSchema):
    name: str
    description: Optional[str] = None
"""
    write_file("app/amenities/schemas.py", amenities_schemas)

    # ==================== app/favorites/schemas.py ====================
    favorites_schemas = """import uuid
from typing import Optional
from pydantic import BaseModel
from app.shared.schemas import BaseResponseSchema
from app.schemas.properties import PropertyResponse

class FavoriteCreate(BaseModel):
    property_id: uuid.UUID

class FavoriteResponse(BaseResponseSchema):
    user_id: uuid.UUID
    property_id: uuid.UUID
    property: Optional[PropertyResponse] = None
"""
    write_file("app/favorites/schemas.py", favorites_schemas)

    # ==================== app/reviews/schemas.py ====================
    reviews_schemas = """import uuid
from typing import Optional
from pydantic import BaseModel, Field
from app.shared.schemas import BaseResponseSchema
from app.schemas.users import UserResponse

class ReviewCreate(BaseModel):
    property_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=5, max_length=1000)

class ReviewResponse(BaseResponseSchema):
    user_id: uuid.UUID
    property_id: uuid.UUID
    rating: int
    comment: str
    user: Optional[UserResponse] = None
"""
    write_file("app/reviews/schemas.py", reviews_schemas)

    # ==================== app/notifications/schemas.py ====================
    notifications_schemas = """import uuid
from pydantic import BaseModel
from app.shared.schemas import BaseResponseSchema

class NotificationCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    message: str
    type: str = "info"

class NotificationResponse(BaseResponseSchema):
    user_id: uuid.UUID
    title: str
    message: str
    type: str
    is_read: bool
"""
    write_file("app/notifications/schemas.py", notifications_schemas)

    print("All schemas successfully migrated into modular structure.")

if __name__ == "__main__":
    migrate_schemas()
