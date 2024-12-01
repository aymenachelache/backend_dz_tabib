# from src.database.connection import create_db_connection
# from src.auth.schemas import Forgetpassword, UserResponse , User,SearchUser
# from datetime import datetime

# def get_user_by_email_or_username(identifier: SearchUser):
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     print(identifier)
#     try:
#         # Query to check if the user already exists
#         cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (identifier.email,identifier.username))
#         user = cursor.fetchone()
#         if user is None:
#             return None
#         user_id,username,password,email,disabled,created_at,reset_token,token_expiry = user
#         user = User(id=user_id,username=username,email=email,password=password,disabled=disabled,created_at=created_at,reset_token=reset_token,token_expiry=token_expiry)
#         print(user)
#         return user
#     finally:
#         cursor.close()
#         connection.close()
    
# def get_user_by_email(email: str):
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     try:
#         # Query to check if the user already exists
#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()
#         if user is None:
#             return None
#         user_id,username,password,email,disabled,created_at,reset_token,token_expiry = user
#         user = User(id=user_id,username=username,email=email,password=password,disabled=disabled,created_at=created_at,reset_token=reset_token,token_expiry=token_expiry)
#         return user
#     finally:
#         cursor.close()
#         connection.close()

# def insert_user(username: str, hashed_password: str, email: str):
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     try:
#         # Insert a new user
#         cursor.execute(
#             "INSERT INTO users (username, password,email) VALUES (%s, %s,%s)",
#             (username, hashed_password,email)
#         )
#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#         raise e
#     finally:
#         cursor.close()
#         connection.close()


# def set_reset_token_in_db(user_id: int,token: str, expiry: datetime):
#     """Set a reset token and expiry in the database."""
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     try:
#         # Update the user record with the reset token and expiry
#         cursor.execute(
#             "INSERT INTO password_resets (user_id, reset_token, expiry) VALUES (%s, %s, %s)",
#             (user_id, token, expiry)
#         )
#         connection.commit()
#         return token, expiry
#     except Exception as e:
#         connection.rollback()
#         return None
#     finally:
#         cursor.close()
#         connection.close()

# def get_user_by_reset_token(token: str):
#     """Verify the reset token."""
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(
#             "SELECT user_id, expiry FROM password_resets WHERE reset_token = %s",
#             (token,)
#         )
#         user = cursor.fetchone()

#         return user
#     finally:
#         cursor.close()
#         connection.close()


# def update_password(hashed_password: str, user_id: str):
#     try:
#         # Update the user's password
#         connection = create_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(
#             "UPDATE users SET password = %s WHERE id = %s",
#             (hashed_password, user_id)
#         )
#         cursor.execute("DELETE FROM password_resets WHERE user_id = %s", [user_id])
#         connection.commit()
#         return
#     except Exception as e:
#         raise e
#     finally:
#         cursor.close()
#         connection.close()


from src.auth.schemas import Forgetpassword, UserFromDB, UserRegister, UserResponse, User, SearchUser, test
from src.database.query_helper import execute_query
from datetime import datetime

def get_user_by_email_or_username(identifier: SearchUser):
    query = "SELECT * FROM users WHERE email = %s OR username = %s"
    params = (identifier.email, identifier.username)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    user_id,username, firstName, lastName, phoneNumber, email, password, is_doctor, created_at, disabled = user
    return User(
        id=user_id,
        username=username,
        firstName=firstName,
        lastName=lastName,
        phoneNumber=phoneNumber,
        email=email,
        password=password,
        is_doctor=is_doctor,
        created_at=created_at

    )

def get_user_by_email(email: str):
    query = "SELECT * FROM users WHERE email = %s"
    params = (email,)
    user = execute_query(query, params, fetch_one=True)
    if user is None:
        return None
    user_id,username, firstName, lastName, phoneNumber, email, password, disabled, created_at, is_doctor = user
    return UserFromDB(
        username=username,
        firstName=firstName,
        lastName=lastName,
        phoneNumber=phoneNumber,
        email=email,
        password=password,
        is_doctor=is_doctor,
        created_at=created_at,
        id=user_id,
        disabled=disabled
    )


# def insert_user(username: str, hashed_password: str, email: str):
#     query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
#     params = (username, hashed_password, email)
#     execute_query(query, params)
def insert_user(user:UserRegister):
    query = "INSERT INTO users (username, firstName, lastName, phoneNumber, email, password, is_doctor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (user.username, user.firstName, user.lastName, user.phoneNumber, user.email, user.password, user.is_doctor)
    execute_query(query, params)

def set_reset_token_in_db(user_id: int, token: str, expiry: datetime):
    query = "INSERT INTO password_resets (user_id, reset_token, expiry) VALUES (%s, %s, %s)"
    params = (user_id, token, expiry)
    execute_query(query, params)

def get_user_by_reset_token(token: str):
    query = "SELECT user_id, expiry FROM password_resets WHERE reset_token = %s"
    params = (token,)
    return execute_query(query, params, fetch_one=True)

def update_password(hashed_password: str, user_id: str):
    update_password_query = "UPDATE users SET password = %s WHERE id = %s"
    print(user_id,hashed_password)
    delete_token_query = "DELETE FROM password_resets WHERE user_id = %s"
    params = (hashed_password, user_id)
    execute_query(update_password_query, params)
    execute_query(delete_token_query, (user_id,))
