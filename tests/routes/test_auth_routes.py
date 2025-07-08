import pytest
import uuid


def test_register_and_login(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "securepassword"
    }

    response = client.post("/auth/register", json=user_data)
    print("REGISTER:", response.status_code, response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = client.post("/auth/login", json={
        "username_or_email": user_data["email"],
        "password": user_data["password"]
    })
    print("LOGIN:", response.status_code, response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()
