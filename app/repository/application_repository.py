from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.application import Application
from app.repository.base_repository import BaseRepository

class ApplicationRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Application)
