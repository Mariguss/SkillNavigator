from app.models.base_model import BaseModelCreatedUpdated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.models.vacancy import Vacancy
    from app.models.user import User

class Application(BaseModelCreatedUpdated):
    __tablename__ = "application"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)

    status: Mapped[str] = mapped_column(nullable=False)
    backup_vacancy_name: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text,nullable=True)

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="applications")
    user: Mapped["User"] = relationship("User", back_populates="applications")
