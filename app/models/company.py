from app.models.base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import List, TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.vacancy import Vacancy

class Company(BaseModelCreatedUpdated):
    __tablename__ = "company"
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    site_url: Mapped[str | None] = mapped_column(nullable=True)

    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", back_populates="company")