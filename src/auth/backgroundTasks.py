import asyncio
from datetime import datetime
from src.database.connection import create_db_connection

async def delete_expired_tokens():
    """Delete expired reset tokens from the database."""
    while True:
        connection = create_db_connection()
        cursor = connection.cursor()
        try:
            now = datetime.now()
            # Delete expired tokens
            cursor.execute("DELETE FROM password_resets WHERE expiry < %s", (now,))
            connection.commit()
        except Exception as e:
            print(f"Error while cleaning expired tokens: {e}")
        finally:
            cursor.close()
            connection.close()
        
        # Sleep for a defined interval (e.g., 1 hour)
        await asyncio.sleep(3600)
