from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.vacancy import Vacancy
from app.repository.base_repository import BaseRepository
from datetime import datetime, timedelta, timezone


class VacancyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Vacancy)

    def archive_old_vacancies(self, days: int = 90) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        with self.session_factory() as session:
            count = (
                session.query(Vacancy)
                .filter(Vacancy.created_at <= cutoff, Vacancy.is_active == True)
                .update({"is_active": False}, synchronize_session=False)
            )
            session.commit()
            return count
    