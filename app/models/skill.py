from app.models.base_model import BaseModelCreated
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.user_skills import UserSkills
    from app.models.vacancy_skills import VacancySkills

class Skill(BaseModelCreated):
    __tablename__ = "skill"
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(nullable=True)

    user_skills: Mapped[List["UserSkills"]] = relationship("UserSkills", back_populates="skill")
    vacancy_skills: Mapped[List["VacancySkills"]] = relationship("VacancySkills", back_populates="skill")