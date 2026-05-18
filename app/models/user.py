from base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List
from application import Application
from user_skills import UserSkills

class User(BaseModel):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    email: Mapped[str]

    applications: Mapped[List["Application"]] = relationship(back_populates="user")
    user_skills: Mapped[List["UserSkills"]] = relationship(back_populates="user")