from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.core.security import get_password_hash
from schemas.user_schema import UpsertUser

class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        self.repository = repository
        super().__init__(repository)

    def add(self, schema):
        user_data = schema.dict()
        if "password" in user_data:
            password = user_data.pop("password")
            user_data["password_hash"] = get_password_hash(password)
        
        updated_schema = UpsertUser(**user_data)
        return self._repository.create(updated_schema)

    def patch(self, id: int, schema):
        
        user_data = schema.dict(exclude_none=True)
        if "password" in user_data:
            password = user_data.pop("password")
            user_data["password_hash"] = get_password_hash(password)
            
        updated_schema = UpsertUser(**user_data)

        return self.repository.update(id, updated_schema)