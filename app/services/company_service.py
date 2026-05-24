from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService

class CompanyService(BaseService):
    def __init__(self, repository: CompanyRepository):
        self.repository = repository
        super().__init__(repository)
    