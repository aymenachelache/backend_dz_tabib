from mysql.connector import connection
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_db_connection():
    """Establish and return a connection to the MySQL database."""
    try:
        cnx = connection.MySQLConnection(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        if cnx.is_connected():
            print("Successfully connected to the database")
        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
