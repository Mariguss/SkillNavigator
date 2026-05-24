from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.vacancy import Vacancy
from app.repository.base_repository import BaseRepository

class VacancyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Vacancy)
    