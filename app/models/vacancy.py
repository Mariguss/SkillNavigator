from app.models.base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from typing import List, TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.application import Application
    from app.models.vacancy_skills import VacancySkills

class Vacancy(BaseModelCreatedUpdated):
    __tablename__ = "vacancy"
    
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
    raw_text: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    company: Mapped["Company"] = relationship("Company", back_populates="vacancies")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="vacancy")
    vacancy_skills: Mapped[List["VacancySkills"]] = relationship("VacancySkills", back_populates="vacancy")
    


