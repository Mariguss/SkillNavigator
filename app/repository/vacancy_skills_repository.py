from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DuplicatedError, NotFoundError
from app.models.vacancy_skills import VacancySkills


class VacancySkillsRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_vacancy_skills(self, vacancy_id: int):
        with self.session_factory() as session:
            return session.query(VacancySkills).filter(VacancySkills.vacancy_id == vacancy_id).all()

    def add_skill(self, vacancy_id: int, skill_id: int) -> VacancySkills:
        with self.session_factory() as session:
            entry = VacancySkills(vacancy_id=vacancy_id, skill_id=skill_id)
            try:
                session.add(entry)
                session.commit()
                session.refresh(entry)
                return entry
            except IntegrityError:
                raise DuplicatedError(detail="Vacancy already has this skill.")

    def remove_skill(self, vacancy_id: int, skill_id: int) -> None:
        with self.session_factory() as session:
            entry = (
                session.query(VacancySkills)
                .filter(VacancySkills.vacancy_id == vacancy_id, VacancySkills.skill_id == skill_id)
                .first()
            )
            if not entry:
                raise NotFoundError(detail="Skill not found in vacancy.")
            session.delete(entry)
            session.commit()

    def get_skill_ids(self, vacancy_id: int) -> set:
        with self.session_factory() as session:
            rows = session.query(VacancySkills.skill_id).filter(VacancySkills.vacancy_id == vacancy_id).all()
            return {r[0] for r in rows}

    def replace_all(self, vacancy_id: int, skill_ids: list[int]) -> None:
        with self.session_factory() as session:
            session.query(VacancySkills).filter(VacancySkills.vacancy_id == vacancy_id).delete()
            for sid in skill_ids:
                session.add(VacancySkills(vacancy_id=vacancy_id, skill_id=sid))
            session.commit()
