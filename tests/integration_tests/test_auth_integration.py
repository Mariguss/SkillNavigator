import pytest
import time

def test_registration_and_login_flow(client):
    """Сквозной тест: регистрация нового пользователя и последующий вход"""
    
    unique_suffix = int(time.time())
    user_data = {
        "login": f"integration_user_{unique_suffix}",
        "email": f"integration_{unique_suffix}@example.com",
        "password": "strongpassword"
    }

    # Шаг 1: Тестируем регистрацию (Sign Up)
    signup_response = client.post("/api/v1/auth/sign-up", json=user_data)
    assert signup_response.status_code in [200, 201]
    
    # Шаг 2: Тестируем успешный вход (Sign In)
    login_data = {
        "login": user_data["login"],
        "password": user_data["password"]
    }
    login_response = client.post("/api/v1/auth/sign-in", json=login_data)
    
    assert login_response.status_code == 200
    response_json = login_response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


def test_login_wrong_credentials(client):
    """Тест авторизации с неверными данными"""
    invalid_login_data = {
        "login": "non_existent_user",
        "password": "wrong_password"
    }
    response = client.post("/api/v1/auth/sign-in", json=invalid_login_data)
    # Код 400, так как твой WrongCredentialsError наследует HTTP_400_BAD_REQUEST
    assert response.status_code == 400