from app.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.skill import Skill

class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"), primary_key=True)

    user: Mapped["User"] = relationship("User", back_populates="user_skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_skills")