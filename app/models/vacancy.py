from base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from typing import List
from company import Company
from application import Application
from vacancy_skills import VacancySkills

class Vacancy(BaseModelCreatedUpdated):
    __tablename__ = "vacancy"
    
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), primary_key=True)

    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    raw_text: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    company: Mapped["Company"] = relationship(back_populates="vacancies")
    applications: Mapped[List["Application"]] = relationship(back_populates="vacancy")
    vacancy_skills: Mapped[List["VacancySkills"]] = relationship(back_populates="vacancy")
    


