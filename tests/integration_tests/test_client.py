def test_client(client):
    response = client.get("/docs")
    assert response.status_code == 200