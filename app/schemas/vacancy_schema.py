from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import SearchOptions, FindBase, ModelBaseInfo


class VacancyBase(BaseModel):

    company_id: int
    title: str
    url: str
    raw_text:  str | None = None
    is_active: bool = True


# То, что мы ждем при создании
class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    company_id: int | None = None
    title: str | None = None
    url: str | None = None
    raw_text:  str | None = None
    is_active: bool | None = None

class Vacancy(VacancyBase):
    ...

class VacancyResponse(Vacancy, ModelBaseInfo):

    model_config = {"from_attributes": True}

class FindVacancy(FindBase):
    company_id__eq: int | None = None
    title__eq: str | None = None
    url__eq: str | None = None
    is_active__eq: bool | None= None

class FindVacancyResult(BaseModel):
    founds: List[VacancyResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}
