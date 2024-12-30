


from src.auth.schemas import Forgetpassword, UserFromDB, UserRegister, UserResponse, User, SearchUser
from src.database.query_helper import execute_query
from datetime import datetime

def get_user_by_email_or_username(identifier: SearchUser):
    query = "SELECT * FROM users WHERE email = %s OR username = %s"
    params = (identifier.email, identifier.username)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    user_id,username, first_name, last_name, phone_number, email, password, is_doctor, created_at, disabled = user
    return User(**user)

def get_user_by_email(email: str):
    query = "SELECT * FROM users WHERE email = %s"
    params = (email,)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    return UserFromDB(**user)

def get_user_by_id(id: int):
    query = "SELECT * FROM users WHERE id = %s"
    params = (id,)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    return UserFromDB(**user)

def get_doctor_by_email(email: str):
    query = """
        SELECT d.*, s.name AS specialization_name 
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        WHERE d.email = %s
    """
    params = (email,)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    return UserFromDB(**user)


def insert_user(user:UserRegister):
    query = "INSERT INTO users (username, first_name, last_name, phone_number, email, password, is_doctor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (user.username, user.first_name, user.last_name, user.phone_number, user.email, user.password, user.is_doctor)
    execute_query(query, params)

def insert_doctor(user:UserRegister):
    query = "INSERT INTO doctors (username, first_name, last_name, phone_number, email, password, is_doctor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (user.username, user.first_name, user.last_name, user.phone_number, user.email, user.password, user.is_doctor)
    execute_query(query, params)

def update_user(user_id: int, user_fields: dict):
    if user_fields:
        user_query = f"""
            UPDATE users
            SET {', '.join([f"{key} = %s" for key in user_fields.keys()])}
            WHERE id = %s
        """
        execute_query(user_query, list(user_fields.values()) + [user_id])

def set_reset_token_in_db(user_id: int, token: str, expiry: datetime):
    query = "INSERT INTO password_resets (user_id, reset_token, expiry) VALUES (%s, %s, %s)"
    params = (user_id, token, expiry)
    execute_query(query, params)

def get_user_by_reset_token(token: str):
    query = "SELECT user_id, expiry FROM password_resets WHERE reset_token = %s"
    params = (token,)
    return execute_query(query, params, fetch_one=True)

def update_user_password(hashed_password: str, user_id: str):
    update_password_query = "UPDATE users SET password = %s WHERE id = %s"
    delete_token_query = "DELETE FROM password_resets WHERE user_id = %s"
    params = (hashed_password, user_id)
    execute_query(update_password_query, params)
    execute_query(delete_token_query, (user_id,))
def update_doctor_password(hashed_password: str, user_id: str):
    update_password_query = "UPDATE doctors SET password = %s WHERE id = %s"
    params = (hashed_password, user_id)
    execute_query(update_password_query, params)