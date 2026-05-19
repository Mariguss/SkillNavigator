from base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from vacancy import Vacancy

class Company(BaseModelCreatedUpdated):
    __tablename__ = "company"
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    site_url: Mapped[str] = mapped_column(nullable=True)

    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="company")