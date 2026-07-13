import math
from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number, starting from 1"),
        size: int = Query(default=20, ge=1, le=100, description="Number of items per page")
    ) -> None:
        self.page = page
        self.size = size

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "Page[T]":
        pages = math.ceil(total / params.size) if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )
