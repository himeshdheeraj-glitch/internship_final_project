import uuid
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
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
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
