from app.repository.vacancy_repository import VacancyRepository
from app.repository.user_skills_repository import UserSkillsRepository
from app.repository.vacancy_skills_repository import VacancySkillsRepository
from app.services.base_service import BaseService


class VacancyService(BaseService):
    def __init__(
        self,
        repository: VacancyRepository,
        user_skills_repository: UserSkillsRepository,
        vacancy_skills_repository: VacancySkillsRepository,
    ) -> None:
        self.repository = repository
        self.user_skills_repository = user_skills_repository
        self.vacancy_skills_repository = vacancy_skills_repository
        super().__init__(repository)

    def get_match_percent(self, user_id: int, vacancy_id: int) -> float:
        user_skill_ids = self.user_skills_repository.get_skill_ids(user_id)
        vacancy_skill_ids = self.vacancy_skills_repository.get_skill_ids(vacancy_id)
        if not vacancy_skill_ids:
            return 0.0
        matched = user_skill_ids & vacancy_skill_ids
        return round(len(matched) / len(vacancy_skill_ids) * 100, 1)
