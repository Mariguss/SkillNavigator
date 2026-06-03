import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth_schema import SignIn, SignUp
from app.schemas.user_schema import UpsertUser
from app.core.exceptions import WrongCredentialsError

# Настройка pytest для работы с асинхронным кодом
# pytestmark = pytest.mark.asyncio


def test_auth_service_sign_in_success():
    """Модульный тест успешной авторизации"""
    # Mock для репозитория
    mock_repo = MagicMock()
    # Имитируем возвращаемое значение метода read_by_options
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.login = "test_user"
    mock_user.email = "test@example.com"
    mock_user.is_superuser = False
    mock_user.password_hash = "hashed_password"  # Заглушка хэша
    
    mock_repo.read_by_options.return_value = {"founds": [mock_user]}

    auth_service = AuthService(repository=mock_repo)
    sign_in_info = SignIn(login="test_user", password="correct_password")

    # Патчим утилиты безопасности, чтобы не вызывать реальный bcrypt
    with patch("app.services.auth_service.verify_password", return_value=True), \
         patch("app.services.auth_service.create_access_token", return_value=("mocked_token", "datetime")):
        
        result = auth_service.sign_in(sign_in_info)
        
        assert result["access_token"] == "mocked_token"
        assert result["token_type"] == "bearer"
        mock_repo.read_by_options.assert_called_once()


def test_auth_service_sign_in_wrong_password():
    """Модульный тест авторизации с неверным паролем"""
    mock_repo = MagicMock()
    mock_user = MagicMock()
    mock_user.password_hash = "hashed_password"
    mock_repo.read_by_options.return_value = {"founds": [mock_user]}

    auth_service = AuthService(repository=mock_repo)
    sign_in_info = SignIn(login="test_user", password="wrong_password")

    with patch("app.services.auth_service.verify_password", return_value=False):
        with pytest.raises(WrongCredentialsError):
            auth_service.sign_in(sign_in_info)


def test_user_service_add():
    """Модульный тест создания пользователя через UserService"""
    mock_repo = MagicMock()
    user_service = UserService(repository=mock_repo)
    
    schema = UpsertUser(
        login="new_user",
        email="new@example.com",
        password="plain_password",
        is_superuser=False
    )

    with patch("app.services.user_service.get_password_hash", return_value="safely_hashed"):
        user_service.add(schema)
        
        # Проверяем, что в репозиторий ушла схема UpsertUserInDB с хэшем вместо пароля
        called_args = mock_repo.create.call_args[0][0]
        assert called_args.password_hash == "safely_hashed"
        assert called_args.login == "new_user"