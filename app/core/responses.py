from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Request completed successfully"
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True
