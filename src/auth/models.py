from src.database.connection import create_db_connection
from src.auth.schemas import Forgetpassword, UserResponse , User,SearchUser
from datetime import datetime

def get_user_by_email_or_username(identifier: SearchUser):
    connection = create_db_connection()
    cursor = connection.cursor()
    print(identifier)
    try:
        # Query to check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (identifier.email,identifier.username))
        user = cursor.fetchone()
        if user is None:
            return None
        user_id,username,password,email,disabled,created_at,reset_token,token_expiry = user
        user = User(id=user_id,username=username,email=email,password=password,disabled=disabled,created_at=created_at,reset_token=reset_token,token_expiry=token_expiry)
        print(user)
        return user
    finally:
        cursor.close()
        connection.close()
    
def get_user_by_email(email: str):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        # Query to check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        user_id,username,password,email,disabled,created_at,reset_token,token_expiry = user
        user = User(id=user_id,username=username,email=email,password=password,disabled=disabled,created_at=created_at,reset_token=reset_token,token_expiry=token_expiry)
        return user
    finally:
        cursor.close()
        connection.close()

def insert_user(username: str, hashed_password: str, email: str):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        # Insert a new user
        cursor.execute(
            "INSERT INTO users (username, password,email) VALUES (%s, %s,%s)",
            (username, hashed_password,email)
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def set_reset_token_in_db(user_id: int,token: str, expiry: datetime):
    """Set a reset token and expiry in the database."""
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        # Update the user record with the reset token and expiry
        cursor.execute(
            "INSERT INTO password_resets (user_id, reset_token, expiry) VALUES (%s, %s, %s)",
            (user_id, token, expiry)
        )
        connection.commit()
        return token, expiry
    except Exception as e:
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def get_user_by_reset_token(token: str):
    """Verify the reset token."""
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT user_id, expiry FROM password_resets WHERE reset_token = %s",
            (token,)
        )
        user = cursor.fetchone()

        return user
    finally:
        cursor.close()
        connection.close()


def update_password(hashed_password: str, user_id: str):
    try:
        # Update the user's password
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (hashed_password, user_id)
        )
        cursor.execute("DELETE FROM password_resets WHERE user_id = %s", [user_id])
        connection.commit()
        return
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()