from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import ModelBaseInfo, SearchOptions, FindBase


class SkillBase(BaseModel):

    name: str
    category: str


# То, что мы ждем от пользователя при создании
class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):

    name: str | None = None # Делаем необязательным, чтобы можно было обновить только URL
    site_url: str | None = None 

class Skill(SkillBase, ModelBaseInfo):
    ...

class SkillResponse(Skill):

    model_config = {"from_attributes": True}

class FindCompany(FindBase):
    name__eq: str | None = None
    url__eq: str | None = None

class FindSkillResult(BaseModel):
    founds: List[SkillResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}