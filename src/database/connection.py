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


def create_db_connection(create_db_if_missing=False):
    """Establish and return a connection to the MySQL database."""
    try:
        # Connect to MySQL server (without specifying the database)
        server_connection = connection.MySQLConnection(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        if server_connection.is_connected():
            print("Successfully connected to the MySQL server")

        # Create the database if it doesn't exist
        if create_db_if_missing:
            cursor = server_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
            print(f"Database `{os.getenv('DB_NAME')}` ensured to exist.")
            cursor.close()

        # Connect to the specific database
        cnx = connection.MySQLConnection(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
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
