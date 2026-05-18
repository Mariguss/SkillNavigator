from base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from skill import Skill
from vacancy import Vacancy

class VacancySkills(Base):
    __tablename__ = "vacancy_skills"

    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"))

    skill: Mapped["Skill"] = relationship(back_populates="vacancy_skills")
    vacancy: Mapped["Vacancy"] = relationship(back_populates="vacancy_skills")
