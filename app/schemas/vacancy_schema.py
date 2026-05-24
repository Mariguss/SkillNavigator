from app.schemas.base_schema import ModelBaseInfo
from pydantic import BaseModel

class VacancyCreate(BaseModel):

    company_id: int
    title: str
    url: str
    raw_text: str
    is_active: bool = True


class VacancyResponse(ModelBaseInfo, VacancyCreate):

    id: int

    model_config = {"from_attributes": True} 


