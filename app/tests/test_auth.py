def test_create_user(client):
    response = client.post(
        "/auth/",
        data={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}


def test_create_user_duplicate(client):
    client.post(
        "/auth/",
        data={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/",
        data={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_for_access_token(client):
    client.post(
        "/auth/",
        data={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/token",
        data={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
