from pydantic import BaseModel
from typing import List
from app.schemas.base_schema import ModelBaseInfo, SearchOptions, FindBase


class CompanyBase(BaseModel):

    name: str
    site_url: str | None = None 


# То, что мы ждем от пользователя при создании
class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):

    name: str | None = None # Делаем необязательным, чтобы можно было обновить только URL
    site_url: str | None = None 

class Company(CompanyBase, ModelBaseInfo):
    ...

class CompanyResponse(Company):

    model_config = {"from_attributes": True}

class FindCompany(FindBase):
    name__eq: str | None = None
    url__eq: str | None = None

class FindCompanyResult(BaseModel):
    founds: List[CompanyResponse]
    search_options: SearchOptions | None

    model_config = {"from_attributes": True}