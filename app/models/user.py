from base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List
from application import Application
from user_skills import UserSkills

class User(BaseModelCreatedUpdated):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    applications: Mapped[List["Application"]] = relationship(back_populates="user")
    user_skills: Mapped[List["UserSkills"]] = relationship(back_populates="user")