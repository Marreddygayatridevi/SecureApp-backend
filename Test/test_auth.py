import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from jose import jwt
from auth import SECRET_KEY, ALGORITHM


client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_test_user():
    yield
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    if user:
        db.delete(user)
        db.commit()
    db.close()


def test_create_user():
    response = client.post(
        "/auth/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "is_active":"true"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert "user_id" in response.json()


def test_login_for_access_token():
    # First, register the user
    client.post(
        "/auth/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "is_active":"true"
        }
    )

    # Then, log in to receive the token
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Optionally decode the token and check payload
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "id" in payload


def test_login_with_invalid_credentials():
    response = client.post(
        "/auth/token",
        data={
            "username": "nonexistentuser",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

