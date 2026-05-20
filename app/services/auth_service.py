from datetime import timedelta
from typing import List
from fastapi import HTTPException

from app.core.config import configs
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.auth_schema import Payload, SignIn, SignUp
from app.schemas.user_schema import FindUser
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        # 1. Создаем базовый объект без валидации
        find_user = FindUser.model_construct(
            login=None,
            email=None,
            ordering=None,
            page=1,
            page_size=1
        )
        # 2. Насильно прописываем параметры в __dict__
        find_user.__dict__["login__eq"] = sign_in_info.login
        
        # Передаем None, чтобы убрать фильтрацию по статусу админа в SQL-запросе
        find_user.__dict__["is_superuser"] = None 
        
        # Дальше твой оригинальный код без изменений:
        user_list_result = self.user_repository.read_by_options(find_user)
        users: List[User] = user_list_result["founds"]
        
        if len(users) < 1:
            raise HTTPException(status_code=400, detail="Incorrect login or password")
        
        found_user = users[0]
        
        if not verify_password(sign_in_info.password, found_user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect login or password")
        
        payload = Payload(
            id=found_user.id,
            email=found_user.email,
            login=found_user.login,
            is_superuser=found_user.is_superuser,
        )
        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expiration": expiration_datetime,
            "user_info": found_user,
        }

    def sign_up(self, user_info: SignUp):
        hashed_password = get_password_hash(user_info.password)
        
        db_user = User(
            login=user_info.login,
            email=user_info.email,
            password_hash=hashed_password,
            is_superuser=False,
        )

        with self.user_repository.session_factory() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            
        return db_user
