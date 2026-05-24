from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService
from app.schemas.company_schema import CompanyCreate, CompanyResponse

class CompanyService(BaseService):
    def __init__(self, repository: CompanyRepository):
        self.repository = repository
        super().__init__(repository)
    
       
    