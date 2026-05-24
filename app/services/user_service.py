from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.core.security import get_password_hash
from app.schemas.user_schema import UpsertUser, UpsertUserInDB

class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        self.repository = repository
        super().__init__(repository)

    def add(self, schema: UpsertUser):
        hashed_password = get_password_hash(schema.password) 
        
        db_schema = UpsertUserInDB(
            login=schema.login,
            email=schema.email,
            is_superuser=schema.is_superuser,
            password_hash=hashed_password
        )
        
        return self._repository.create(db_schema)


    def patch(self, id: int, schema: UpsertUser):
        hashed_password = get_password_hash(schema.password) if schema.password else None
        
        db_schema = UpsertUserInDB(
            login=schema.login,
            email=schema.email,
            is_superuser=schema.is_superuser,
            password_hash=hashed_password
        )
        
        return self.repository.update(id, db_schema)
