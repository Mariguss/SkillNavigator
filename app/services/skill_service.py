from app.repository.skill_repository import SkillRepository
from app.services.base_service import BaseService

class SkillService(BaseService):
    def __init__(self, repository: SkillRepository):
        self.repository = repository
        super().__init__(repository)
    