from app.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.vacancy import Vacancy

class VacancySkills(Base):
    __tablename__ = "vacancy_skills"

    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"),primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"),primary_key=True)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="vacancy_skills")
    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="vacancy_skills")
