from app.repository.vacancy_repository import VacancyRepository
from app.services.base_service import BaseService

class VacancyService(BaseService):
    def __init__(self, repository: VacancyRepository):
        self.repository = repository
        super().__init__(repository)