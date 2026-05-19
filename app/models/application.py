from base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from vacancy import Vacancy
from user import User

class Application(BaseModelCreatedUpdated):
    __tablename__ = "application"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), primary_key=True)

    status: Mapped[str] = mapped_column(nullable=False)
    backup_vacancy_name: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text,nullable=True)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="applications")
    user: Mapped["User"] = relationship(back_populates="applications")
