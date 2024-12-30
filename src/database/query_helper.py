from src.database.connection import create_db_connection

def execute_query(query: str, params: tuple = (), fetch_one=False, fetch_all=False, return_last_id=False,check_rows_affected=False):
    """Execute a database query with provided parameters."""
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch_one:
            return cursor.fetchone()
        
        if fetch_all:
            return cursor.fetchall()

        connection.commit()
        if return_last_id:
            connection.commit()  # Commit changes if it's an insert
            return cursor.lastrowid  # Get the last inserted ID (MySQL-specific)

        if check_rows_affected:
            return cursor.rowcount > 0
        
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()



