from src.database.connection import create_db_connection

def execute_query(query: str, params: tuple = (), fetch_one=False, fetch_all=False):
    """Execute a database query with provided parameters."""
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()



