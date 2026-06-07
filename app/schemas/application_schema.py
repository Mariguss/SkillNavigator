from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import ModelBaseInfo, SearchOptions, FindBase


class ApplicationBase(BaseModel):

    user_id: int
    vacancy_id: int
    status: str
    backup_vacancy_name: str
    notes: str | None = None


# То, что мы ждем от пользователя при создании
class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):

    status: str | None = None
    notes: str | None = None

class Application(ApplicationBase, ModelBaseInfo):
    ...

class ApplicationResponse(Application):

    model_config = {"from_attributes": True}

class FindApplication(FindBase):
    user_id__eq: int | None = None
    vacancy_id__eq: int | None = None
    status__eq: str | None = None

class FindApplicationResult(BaseModel):
    founds: List[ApplicationResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}
