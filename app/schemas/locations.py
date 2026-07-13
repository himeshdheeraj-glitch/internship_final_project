import uuid
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
