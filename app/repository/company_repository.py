from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.company import Company
from app.repository.base_repository import BaseRepository

class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Company)
