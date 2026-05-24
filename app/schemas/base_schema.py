from datetime import datetime
from typing import Any
from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

class ModelBaseInfoWithoutUpdatedAt(BaseModel):
    id: int
    created_at: datetime

class FindBase(BaseModel):
    ordering: str | None = None
    page: int | None = None
    page_size: int | str | None = None


class SearchOptions(FindBase):
    total_count: int | None = None


class FindResult(BaseModel):
    founds: list[Any] | None = None
    search_options: SearchOptions | None = None


class FindDateRange(BaseModel):
    created_at__lt: str | None = None
    created_at__lte: str | None = None
    created_at__gt: str | None = None
    created_at__gte: str | None = None


class Blank(BaseModel):
    pass
