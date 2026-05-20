from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.user_schema import User


class SignIn(BaseModel):
    login: str
    password: str


class SignUp(BaseModel):
    email: EmailStr  # Автоматическая валидация корректности почты
    password: str = Field(..., min_length=6)
    login: str = Field(..., min_length=3, max_length=50)


class Payload(BaseModel):
    id: int
    email: str
    login: str
    is_superuser: bool


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Стандарт для OAuth2/JWT в FastAPI
    expiration: datetime
    user_info: User
