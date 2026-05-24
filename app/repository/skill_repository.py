from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.repository.base_repository import BaseRepository

class SkillRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Skill)