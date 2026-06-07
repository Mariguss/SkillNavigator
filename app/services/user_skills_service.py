from app.repository.user_skills_repository import UserSkillsRepository
from app.repository.skill_repository import SkillRepository


class UserSkillsService:
    def __init__(
        self,
        user_skills_repository: UserSkillsRepository,
        skill_repository: SkillRepository,
    ) -> None:
        self.user_skills_repository = user_skills_repository
        self.skill_repository = skill_repository

    def get_skills(self, user_id: int) -> list:
        entries = self.user_skills_repository.get_user_skills(user_id)
        result = []
        for entry in entries:
            skill = self.skill_repository.read_by_id(entry.skill_id)
            result.append({"id": entry.skill_id, "name": skill.name, "category": skill.category})
        return result

    def add_skill(self, user_id: int, skill_id: int) -> dict:
        self.skill_repository.read_by_id(skill_id)
        entry = self.user_skills_repository.add_skill(user_id, skill_id)
        return {"user_id": entry.user_id, "skill_id": entry.skill_id}

    def remove_skill(self, user_id: int, skill_id: int) -> None:
        self.user_skills_repository.remove_skill(user_id, skill_id)
