from dbutils.pooled_db import PooledDB
import pymysql
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Create a connection pool
connection_pool = PooledDB(
    creator=pymysql,  # Use PyMySQL as the connector
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    mincached=2,  # Minimum number of idle connections in the pool
    maxcached=5,  # Maximum number of idle connections in the pool
    maxconnections=5,  # Maximum number of connections in the pool
    blocking=True,  # Block and wait if no connections are available
)


def get_connection():
    """Get a connection from the pool."""
    try:
        return connection_pool.connection()  # Correct method
    except Exception as e:
        raise Exception(f"Failed to get a connection: {e}")


def execute_query(
    query: str,
    params: tuple = (),
    fetch_one=False,
    fetch_all=False,
    return_last_id=False,
    check_rows_affected=False,
):
    """Execute a database query with provided parameters."""
    connection = get_connection()
    cursor = connection.cursor(
        pymysql.cursors.DictCursor
    )  # Return results as dictionaries
    try:
        cursor.execute(query, params)

        # Fetch results if required
        if fetch_one:
            return cursor.fetchone()

        if fetch_all:
            return cursor.fetchall()

        # Commit changes for INSERT/UPDATE/DELETE
        connection.commit()

        # Return the last inserted ID if required
        if return_last_id:
            return cursor.lastrowid

        # Check if rows were affected
        if check_rows_affected:
            return cursor.rowcount > 0

    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()  # Return the connection to the pool
