# from mysql.connector import connection
# import mysql.connector
# from mysql.connector import errorcode
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()


# def create_db_connection():
#     """Establish and return a connection to the MySQL database."""
#     try:
#         cnx = connection.MySQLConnection(
#             host=os.getenv("DB_HOST"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             database=os.getenv("DB_NAME"),
#         )
#         if cnx.is_connected():
#             print("Successfully connected to the database")
#         return cnx

#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Invalid username or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#         return None

from mysql.connector import connection, errorcode
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_db_connection(create_db_if_missing=False, test=False):
    """Establish and return a connection to the PostgreSQL database."""
    test_mode = os.getenv("TEST_MODE", "False").lower() == "true"
    if test_mode or test:
        db_host = os.getenv("DB_TEST_HOST")
        db_user = os.getenv("DB_TEST_USER")
        db_password = os.getenv("DB_TEST_PASSWORD")
        db_name = os.getenv("DB_TEST_NAME")
    else:
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
    try:
        # Connect to MySQL server (without specifying the database)
        server_connection = connection.MySQLConnection(
            host=db_host,
            user=db_user,
            password=db_password,
        )
        if server_connection.is_connected():
            print("Successfully connected to the MySQL server")

        # Create the database if it doesn't exist
        if create_db_if_missing:
            cursor = server_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database `{db_name}` ensured to exist.")
            cursor.close()

        # Connect to the specific database
        cnx = connection.MySQLConnection(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        )
        if cnx.is_connected():
            print(f"Successfully connected to the database `{os.getenv('DB_NAME')}`")
        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            
        return None 
