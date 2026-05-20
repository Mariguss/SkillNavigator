from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseUser(BaseModel):
    login: str
    email: EmailStr
    is_superuser: bool = False

    class Config:
        from_attributes = True


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    login__eq: str | None = None
    email__eq: str | None = None


class UpsertUser(BaseUser, metaclass=AllOptional):
    password: str | None = None


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
