import os
import pytest
from fastapi.testclient import TestClient
from src.database.connection import create_db_connection
from src.database.db_setup import initialize_database
from src.main import app  # Adjust the import to match your FastAPI app instance

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def set_test_mode():
    os.environ["TEST_MODE"] = "True"
    yield
    os.environ["TEST_MODE"] = "False"


def clean_test_database():
    """Clean up the test database before each test."""
    conn = create_db_connection(test=True)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM doctors")
    cursor.execute("DELETE FROM appointments")
    conn.commit()
    cursor.close()
    conn.close()

@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Clean and initialize the test database before each test."""
    initialize_database(test=True)
    clean_test_database()
    

class TestRegisterUser:
    @pytest.fixture
    def setup(self, setup_test_database):
        pass

    def test_register_user_success(self):
        """Test successful user registration"""
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "testuser@example.com",
                "password": "password123",
                "is_doctor": False,
            },
        )
        assert response.status_code == 200
        assert response.json()["msg"] == "Registered successfully"

    def test_register_user_missing_fields(self):
        """Test registration with missing required fields"""
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "first_name": "Test",
                "email": "testuser@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 422
        errors = response.json()["detail"]
        expected_missing_fields = {"last_name", "phone_number"}
        error_fields = {error["loc"][-1] for error in errors}
        assert expected_missing_fields == error_fields
        for error in errors:
            assert error["type"] == "missing"
            assert error["msg"] == "Field required"

    def test_register_user_invalid_email(self):
        """Test registration with an invalid email format"""
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "invalid_email",
                "password": "password123",
                "is_doctor": True,
            },
        )
        assert response.status_code == 422
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == "value_error"
        assert error_detail["loc"] == ["body", "email"]
        assert error_detail["msg"] == "value is not a valid email address: An email address must have an @-sign."
        assert error_detail["ctx"]["reason"] == "An email address must have an @-sign."

    def test_register_user_duplicate_email(self):
        """Test registration with an existing email"""
        client.post(
            "/register",
            json={
                "username": "testuser1",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "duplicate@example.com",
                "password": "password123",
                "is_doctor": True,
            },
        )
        response = client.post(
            "/register",
            json={
                "username": "testuser2",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "duplicate@example.com",
                "password": "password123",
                "is_doctor": True,
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username or email already taken"

class TestLogin:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, setup_test_database):
        # Register a user for login tests
        client.post(
            "/register",
            json={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "testuser@example.com",
                "password": "password123",
                "is_doctor": False,
            },
        )

    def test_login_success(self):
        """Test successful login"""
        response = client.post(
            "/token",
            data={"username": "testuser@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_failure_wrong_credentials(self):
        """Test login with wrong credentials"""
        response = client.post(
            "/token",
            data={"username": "wronguser@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    def test_login_failure_missing_fields(self):
        """Test login with missing fields"""
        response = client.post(
            "/token",
            data={"username": "", "password": ""},
        )
        assert response.status_code == 401  # FastAPI returns 422 for validation errors


class TestProtectedRoutes:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, setup_test_database):
        # Register a user and log in to get a token
        client.post(
            "/register",
            json={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "email": "testuser@example.com",
                "password": "password123",
                "is_doctor": False,
            },
        )
        self.headers = self.get_auth_headers()

    @staticmethod
    def get_auth_headers():
        """Get authentication headers for protected routes."""
        response = client.post(
            "/token",
            data={"username": "testuser@example.com", "password": "password123"},
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_protected_route_success(self):
        """Test accessing a protected route with a valid token."""
        response = client.get("/users/me/", headers=self.headers)
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@example.com"

    def test_protected_route_unauthorized(self, setup_test_database):
        """Test accessing a protected route without a token."""
        response = client.get("/users/me/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_protected_route_invalid_token(self):
        """Test accessing a protected route with an invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me/", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"