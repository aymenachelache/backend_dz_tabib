# from .connection import create_db_connection


# def create_tables():
#     """Create tables if they don't already exist."""
#     create_doctors_table = """
#     CREATE TABLE IF NOT EXISTS doctors (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         name VARCHAR(255) NOT NULL,
#         specialty VARCHAR(255) NOT NULL,
#         contact VARCHAR(255),
#         email VARCHAR(255) UNIQUE
#     );
#     """
#     create_users_table = """
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(255) UNIQUE NOT NULL,
#         password VARCHAR(255) NOT NULL,
#         email VARCHAR(255) UNIQUE,
#         disabled BOOLEAN DEFAULT FALSE,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         reset_token VARCHAR(255),
#         token_expiry DATETIME
#     );
#     """
#     create_reset_token_table = """
#     CREATE TABLE IF NOT EXISTS password_resets (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     reset_token VARCHAR(255) NOT NULL,
#     expiry DATETIME NOT NULL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#     );
#     """
#     # Add more table definitions as needed...

#     # Connect to the database and execute the table creation queries
#     connection = create_db_connection()
#     if connection:
#         cursor = connection.cursor()
#         try:
#             cursor.execute(create_doctors_table)
#             cursor.execute(create_users_table)
#             cursor.execute(create_reset_token_table)

#             # Execute additional queries for other tables as needed
#             print("Tables created successfully.")
#         except Exception as e:
#             print("Error creating tables:", e)
#         finally:
#             cursor.close()
#             connection.close()


from .connection import create_db_connection


def initialize_database():
    """Initialize the database and create tables if they don't already exist."""
    # Ensure database exists
    connection = create_db_connection(create_db_if_missing=True)
    if connection:
        cursor = connection.cursor()

        # SQL queries for table creation
        create_doctors_table = """
        CREATE TABLE IF NOT EXISTS doctors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            specialty VARCHAR(255) NOT NULL,
            contact VARCHAR(255),
            email VARCHAR(255) UNIQUE
        );
        """
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            phoneNumber VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255) NOT NULL,
            disabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_doctor TINYINT(1) DEFAULT 0
        ); 
        """
        create_reset_token_table = """
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            reset_token VARCHAR(255) NOT NULL,
            expiry DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

        # Execute queries
        try:
            cursor.execute(create_doctors_table)
            cursor.execute(create_users_table)
            cursor.execute(create_reset_token_table)
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)
        finally:
            cursor.close()
            connection.close()
