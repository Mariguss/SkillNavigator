from base_model import BaseModelCreated
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List
from user_skills import UserSkills
from vacancy_skills import VacancySkills

class Skill(BaseModelCreated):
    __tablename__ = "skill"
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    category: Mapped[str] = mapped_column(nullable=True)

    user_skills: Mapped[List["UserSkills"]] = relationship(back_populates="skill")
    vacancy_skills: Mapped[List["VacancySkills"]] = relationship(back_populates="skill")