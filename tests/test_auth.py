# from fastapi.testclient import TestClient
# from src.main import app  # Adjust the import to match your FastAPI app instance

# client = TestClient(app)


# def test_register_user():
#     response = client.post(
#         "/register",
#         json={
#             "username": "testuser",
#             "first_name": "Test",
#             "last_name": "User",
#             "phone_number": "1234567890",
#             "email": "testuser@example.com",
#             "password": "password123",
#             "is_doctor": True
#         }
#     )
#     assert response.status_code == 200 
#     assert response.json()["msg"] == "Registered successfully"

# def test_login_success():
#     # Prepare valid login credentials
#     response = client.post(
#         "/token",
#         data={"username": "testuser@example.com", "password": "password123"}
#     )

#     # Assert that the response is 200 OK
#     assert response.status_code == 200

#     # Assert that the response contains an access token
#     data = response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"
#     return data["access_token"]


# def test_login_failure():
#     # Prepare invalid login credentials
#     response = client.post(
#         "/token",
#         data={"username": "wronguser@example.com", "password": "wrongpassword"}
#     )

#     # Assert that the response is 401 Unauthorized
#     assert response.status_code == 401

#     # Assert the error message
#     data = response.json()
#     assert data["detail"] == "Invalid email or password"

# class TestProtectedGetRoutes:
#     @staticmethod
#     def get_auth_headers():
#         token = test_login_success()
#         return {"Authorization": f"Bearer {token}"}

#     def test_protected_route_1(self):
#         headers = self.get_auth_headers()
#         response = client.get("/users/me/", headers=headers)
#         assert response.status_code == 200

#     def test_protected_route_2(self):
#         headers = self.get_auth_headers()
#         response = client.get("/doctor", headers=headers)
#         assert response.status_code == 200

#     def test_protected_route_2(self):
#         headers = self.get_auth_headers()
#         response = client.get("/user/appointments", headers=headers)
#         assert response.status_code == 200 or response.status_code == 404

from fastapi.testclient import TestClient
import pytest
from src.database.connection import create_db_connection
from src.database.db_setup import initialize_database
from src.main import app  # Adjust the import to match your FastAPI app instance
import os

os.environ["DB_NAME"] = os.getenv("DB_TEST_NAME", "dz_tabib_test")

client = TestClient(app)

initialize_database()

@pytest.fixture(scope="function", autouse=True)
def clean_test_database():
    """Clean up the test database before each test."""
    conn = create_db_connection(test_mode=True)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM doctors")
    cursor.execute("DELETE FROM appointments")
    conn.commit()
    cursor.close()
    conn.close()


# === Test Registration ===
class TestRegisterUser:
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

        # Check for missing fields in the errors list
        expected_missing_fields = {"last_name", "phone_number"}
        error_fields = {error["loc"][-1] for error in errors}
        assert expected_missing_fields == error_fields

        # Check that each error has the correct type and message
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
                "email": "hhhhhh",  # Invalid email
                "password": "password123",
                "is_doctor": True
            }
        )
        
        # Assert the response status
        assert response.status_code == 422

        # Extract the detail from the response
        error_detail = response.json()["detail"][0]

        # Assert the error details
        assert error_detail["type"] == "value_error"
        assert error_detail["loc"] == ["body", "email"]
        assert error_detail["msg"] == "value is not a valid email address: An email address must have an @-sign."
        assert error_detail["ctx"]["reason"] == "An email address must have an @-sign."


    def test_register_user_duplicate_email(self):
        """Test registration with an existing email"""
        # Register the first user
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

        # Try registering with the same email
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


# === Test Login ===
class TestLogin:
    def test_login_success(self):
        # Prepare valid login credentials
        response = client.post(
            "/token",
            data={"username": "testuser@example.com", "password": "password123"}
        )

        # Assert that the response is 200 OK
        assert response.status_code == 200

        # Assert that the response contains an access token
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        return data["access_token"]

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
        assert response.status_code == 401


# === Test Protected Routes ===
class TestProtectedRoutes:
    @staticmethod
    def get_auth_headers():
        """Helper function to get valid authorization headers"""
        response = client.post(
            "/token",
            data={"username": "testuser@example.com", "password": "password123"},
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_protected_route_success(self):
        """Test accessing a protected route with valid token"""
        headers = self.get_auth_headers()
        response = client.get("/users/me/", headers=headers)
        assert response.status_code == 200

    def test_protected_route_unauthorized(self):
        """Test accessing a protected route without a token"""
        response = client.get("/users/me/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_protected_route_invalid_token(self):
        """Test accessing a protected route with an invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me/", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"


