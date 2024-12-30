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
            username VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255) NOT NULL,
            disabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_doctor TINYINT(1) DEFAULT 0,
            years_of_experience INT,
            state VARCHAR(255),
            city VARCHAR(255),
            street VARCHAR(255),
            spoken_languages TEXT,
            zoom_link VARCHAR(255),
            daily_visit_limit INT,
            photo VARCHAR(255),
            specialization_id INT,
            latitude DOUBLE,
            longitude DOUBLE,
            FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE
        );
        """
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(255) NOT NULL,
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
        create_working_days_table = """
        CREATE TABLE IF NOT EXISTS working_days (
            day_id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for the working day
            doctor_id INT NOT NULL,                      -- Foreign key to doctors table
            day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,  -- Day of the week
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
            daily_appointment_limit INT NOT NULL DEFAULT 0  -- Maximum number of appointments per day
        );
        """
        create_working_hours_table = """
        CREATE TABLE IF NOT EXISTS working_hours (
            hour_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique ID for the working hour
            day_id INT NOT NULL,                         -- Foreign key to working_days table
            start_time TIME NOT NULL,                    -- Start time of the shift
            end_time TIME NOT NULL,                      -- End time of the shift
            FOREIGN KEY (day_id) REFERENCES working_days(day_id) ON DELETE CASCADE
        );
        """
        create_appointments_table = """
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique appointment ID
            doctor_id INT NOT NULL,                           -- Foreign key to doctors table
            patient_id INT NOT NULL,                          -- Foreign key to users table
            appointment_date DATE NOT NULL,                  -- Date of the appointment
            appointment_time TIME NOT NULL,                  -- Time of the appointment
            appointment_type ENUM('online', 'présentiel') NOT NULL,  -- Type of appointment
            status ENUM('pending', 'confirmed', 'cancelled', 'completed') NOT NULL DEFAULT 'pending', -- Appointment status
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
        create_specializations_table = """
        CREATE TABLE IF NOT EXISTS specializations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
        create_assurance_table = """
        CREATE TABLE IF NOT EXISTS assurance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
        create_doctor_assurance_table = """
        CREATE TABLE IF NOT EXISTS doctor_assurance (
            doctor_id INT,
            assurance_id INT,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
            FOREIGN KEY (assurance_id) REFERENCES assurance(id) ON DELETE CASCADE,
            PRIMARY KEY (doctor_id, assurance_id)
        );
        """
        create_review_table = """
        CREATE TABLE IF NOT EXISTS review (
            ID_review INT AUTO_INCREMENT PRIMARY KEY,
            note INT CHECK (note <= 5) NOT NULL,
            comment VARCHAR(500)
        );
        """
        create_evaluate_table = """
        CREATE TABLE IF NOT EXISTS evaluate (
            patient_id INT,
            doctor_id INT,
            review_id INT,
            FOREIGN KEY (patient_id) REFERENCES users(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (review_id) REFERENCES review(ID_review),
            PRIMARY KEY (patient_id, doctor_id, review_id)
        );
        """

        # Execute queries
        try:
            cursor.execute(create_specializations_table)
            cursor.execute(create_doctors_table)
            cursor.execute(create_users_table)
            cursor.execute(create_reset_token_table)
            cursor.execute(create_working_days_table)
            cursor.execute(create_working_hours_table)
            cursor.execute(create_appointments_table)
            cursor.execute(create_assurance_table)
            cursor.execute(create_doctor_assurance_table)
            cursor.execute(create_review_table)
            cursor.execute(create_evaluate_table)
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)
        finally:
            cursor.close()
            connection.close()
