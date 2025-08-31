import pytest
from fastapi import status


class TestAuth:
    """Test authentication endpoints."""

    def test_signup_success(self, client):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
        }

        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "id" in data
        assert "hashed_password" not in data

    def test_signup_duplicate_email(self, client, test_user):
        """Test signup with duplicate email."""
        user_data = {
            "email": "test@example.com",  # Same as test_user
            "username": "differentuser",
            "password": "password123",
        }

        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]

    def test_signup_duplicate_username(self, client, test_user):
        """Test signup with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": "testuser",  # Same as test_user
            "password": "password123",
        }

        response = client.post("/api/v1/auth/signup", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already taken" in response.json()["detail"]

    def test_login_success(self, client, test_user):
        """Test successful login."""
        login_data = {"username": "testuser", "password": "testpassword"}

        response = client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_username(self, client):
        """Test login with invalid username."""
        login_data = {"username": "nonexistentuser", "password": "testpassword"}

        response = client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password."""
        login_data = {"username": "testuser", "password": "wrongpassword"}

        response = client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in response.json()["detail"]

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
