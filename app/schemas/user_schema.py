from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.schemas.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional

class BaseUser(BaseModel):
    login: str
    email: EmailStr
    is_superuser: bool = False
    
    model_config = {"from_attributes": True} 


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    pass


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    login__eq: str | None = None
    email__eq: str | None = None


class UpsertUser(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    is_superuser: bool | None = None
    password: str | None = None

    model_config = {"from_attributes": True}


class UpsertUserInDB(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    is_superuser: bool | None = None
    password_hash: str | None = None

    model_config = {"from_attributes": True}


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
