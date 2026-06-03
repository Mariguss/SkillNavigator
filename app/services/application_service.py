from app.repository.application_repository import ApplicationRepository
from app.services.base_service import BaseService

class ApplicationService(BaseService):
    def __init__(self, repository: ApplicationRepository):
        self.repository = repository
        super().__init__(repository)
    