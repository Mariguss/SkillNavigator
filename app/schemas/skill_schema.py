from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import ModelBaseInfoWithoutUpdatedAt, SearchOptions, FindBase


class SkillBase(BaseModel):

    name: str
    category: str


# То, что мы ждем от пользователя при создании
class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):

    name: str | None = None 
    category: str | None = None 

class Skill(SkillBase, ModelBaseInfoWithoutUpdatedAt):
    ...

class SkillResponse(Skill):

    model_config = {"from_attributes": True}

class FindSkill(FindBase):
    name__eq: str | None = None
    category__eq: str | None = None

class FindSkillResult(BaseModel):
    founds: List[SkillResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}