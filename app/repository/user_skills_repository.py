from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DuplicatedError, NotFoundError
from app.models.user_skills import UserSkills


class UserSkillsRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_user_skills(self, user_id: int):
        with self.session_factory() as session:
            return session.query(UserSkills).filter(UserSkills.user_id == user_id).all()

    def add_skill(self, user_id: int, skill_id: int) -> UserSkills:
        with self.session_factory() as session:
            entry = UserSkills(user_id=user_id, skill_id=skill_id)
            try:
                session.add(entry)
                session.commit()
                session.refresh(entry)
                return entry
            except IntegrityError:
                raise DuplicatedError(detail="User already has this skill.")

    def remove_skill(self, user_id: int, skill_id: int) -> None:
        with self.session_factory() as session:
            entry = (
                session.query(UserSkills)
                .filter(UserSkills.user_id == user_id, UserSkills.skill_id == skill_id)
                .first()
            )
            if not entry:
                raise NotFoundError(detail="Skill not found in user profile.")
            session.delete(entry)
            session.commit()

    def get_skill_ids(self, user_id: int) -> set:
        with self.session_factory() as session:
            rows = session.query(UserSkills.skill_id).filter(UserSkills.user_id == user_id).all()
            return {r[0] for r in rows}
