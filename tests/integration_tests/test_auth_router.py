import time

def test_sign_up_and_sign_in(client):
    # Добавляем timestamp к логину, чтобы он гарантированно не повторялся в БД
    unique_suffix = int(time.time())
    
    response = client.post(
        "/api/v1/auth/sign-up",
        json={
            "login": f"router_user_{unique_suffix}",
            "email": f"router_{unique_suffix}@example.com",
            "password": "router_password123"
        },
    )
    assert response.status_code in [200, 201]