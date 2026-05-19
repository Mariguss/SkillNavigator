from pydantic import BaseModel
from typing import Optional

# То, что мы ждем от пользователя при создании
class CompanyCreate(BaseModel):
    name: str
    site_url: Optional[str] = None

# То, что бэкенд возвращает обратно
class CompanyResponse(CompanyCreate):
    id: int

    class Config:
        from_attributes = True  # Чтобы Pydantic понимал объекты SQLAlchemy