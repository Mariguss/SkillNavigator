from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.core.security import get_password_hash

class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def add(self, schema):
        user_data = schema.dict()
        if "password" in user_data:
            password = user_data.pop("password")
            user_data["password_hash"] = get_password_hash(password)
            
        db_user = self.user_repository.model(**user_data)
        
        with self.user_repository.session_factory() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user

    def patch(self, id: int, schema):
        user_data = schema.dict(exclude_none=True)
        
        if "password" in user_data:
            password = user_data.pop("password")
            user_data["password_hash"] = get_password_hash(password)
            
        with self.user_repository.session_factory() as session:
            session.query(self.user_repository.model).filter(self.user_repository.model.id == id).update(user_data)
            session.commit()
            
        return self.user_repository.read_by_id(id)