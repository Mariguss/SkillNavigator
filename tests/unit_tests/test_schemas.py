import pytest
from pydantic import ValidationError
from app.schemas.user_schema import UpsertUser, UpsertUserInDB

def test_upsert_user_valid_email():
    """Проверка валидации корректного EmailStr"""
    user = UpsertUser(login="user1", email="correct@email.com", password="123")
    assert user.email == "correct@email.com"

def test_upsert_user_invalid_email():
    """Проверка выброса ошибки при некорректном формате email"""
    with pytest.raises(ValidationError):
        UpsertUser(login="user1", email="not-an-email", password="123")

def test_upsert_user_in_db_fields():
    """Проверка схемы UpsertUserInDB на чтение полей бэкенда"""
    db_schema = UpsertUserInDB(login="db_user", password_hash="secret_hash")
    assert db_schema.password_hash == "secret_hash"
    # Поля, которые не переданы, должны оставаться None
    assert db_schema.email is None