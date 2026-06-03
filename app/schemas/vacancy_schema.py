from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import SearchOptions, FindBase


class VacancyBase(BaseModel):

    title: str
    url: str
    raw_text:  str | None
    is_active: bool = True


# То, что мы ждем при создании
class VacancyCreate(VacancyBase):
    pass


class Vacancypdate(BaseModel):

    title: str | None
    url: str | None
    raw_text:  str | None
    is_active: bool | None

class Vacancy(VacancyBase):
    ...

class VacancyResponse(Vacancy):

    model_config = {"from_attributes": True}

class FindVacancy(FindBase):
    title__eq: str | None = None
    url__eq: str | None = None
    is_active__eq: bool | None

class FindVacancyResult(BaseModel):
    founds: List[VacancyResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}