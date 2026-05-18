from base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from user import User
from skill import Skill

class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.id"))

    user: Mapped["User"] = relationship(back_populates="user_skills")
    skill: Mapped["Skill"] = relationship(back_populates="user_skills")