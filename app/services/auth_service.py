from datetime import timedelta
from typing import List

from app.core.config import configs
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.auth_schema import Payload, SignIn, SignUp, FindUserByLogin
from app.schemas.user_schema import UpsertUserInDB
from app.services.base_service import BaseService
from app.core.exceptions import WrongCredentialsError

import logging

# Инициализация логгера для текущего модуля
logger = logging.getLogger(__name__)

class AuthService(BaseService):
    def __init__(self, repository: UserRepository):
        self.repository = repository
        super().__init__(repository)

    def sign_in(self, sign_in_info: SignIn):

        find_user = FindUserByLogin(
            login__eq=sign_in_info.login
        )
        
        user_list_result = self.repository.read_by_options(find_user)
        users: List[User] = user_list_result["founds"]
        
        if len(users) < 1:
            logger.warning(f"Failed login attempt for user: {sign_in_info.login}")
            raise WrongCredentialsError(detail="Incorrect login or password")

        found_user = users[0]
        
        if not verify_password(sign_in_info.password, found_user.password_hash):
            logger.warning(f"Failed login attempt for user: {sign_in_info.login}")
            raise WrongCredentialsError(detail="Incorrect login or password")

        payload = Payload(
            id=found_user.id,
            email=found_user.email,
            login=found_user.login,
            is_superuser=found_user.is_superuser,
        )
        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        
        logger.info(f"User successfully authenticated: {found_user.login}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expiration": expiration_datetime,
            "user_info": found_user,
        }

    def sign_up(self, user_info: SignUp):
        # 1. Превращаем SignUp (с полем password) в словарь
        user_data = user_info.model_dump(exclude_none=True)
        
        # 2. Вырезаем чистый пароль и хэшируем его
        password = user_data.pop("password", None)
        hashed_password = get_password_hash(password) if password else None
        
        # 3. Собираем схему для базы данных с password_hash
        db_schema = UpsertUserInDB(
            login=user_data.get("login"),
            email=user_data.get("email"),
            is_superuser=user_data.get("is_superuser", False),
            password_hash=hashed_password
        )
        
        logger.info(f"New user registration initiated: {db_schema.login}")
        # 4. Передаем в репозиторий схему, содержащую password_hash
        return self.repository.create(db_schema)
