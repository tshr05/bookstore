import pytest
from fastapi.testclient import TestClient
from bookstore.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_signup(client: TestClient):
    """Test user signup"""
    response = client.post("/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200

def test_login(client: TestClient):
    """Test user login"""
    response = client.post("/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
