from app.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.vacancy import Vacancy

class VacancySkills(Base):
    __tablename__ = "vacancy_skills"
    __table_args__ = (UniqueConstraint("vacancy_id", "skill_id", name="uq_vacancy_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"), nullable=False)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="vacancy_skills")
    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="vacancy_skills")
