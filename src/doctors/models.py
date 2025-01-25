from fastapi import HTTPException
from src.database.query_helper import execute_query
from datetime import datetime

from src.doctors.schemas import WorkingDay


def update_doctor(doctor_id: int, profile_data: dict, user_id: int, user_fields: dict):
    filtered_data = {
        key: value for key, value in profile_data.items() if key != "assurances"
    }

    if user_fields:
        user_query = f"""
            UPDATE users
            SET {', '.join([f"{key} = %s" for key in user_fields.keys()])}
            WHERE id = %s
        """
        execute_query(user_query, list(user_fields.values()) + [user_id])

    if "specialization_id" in filtered_data:
        specialization_query = "SELECT id FROM specializations WHERE id = %s"
        specialization_exists = execute_query(
            specialization_query, (filtered_data["specialization_id"],), fetch_one=True
        )
        if not specialization_exists:
            raise HTTPException(status_code=400, detail="Invalid specialization ID")
    if filtered_data:
        doctor_query = f"""
            UPDATE doctors
            SET {', '.join([f"{key} = %s" for key in filtered_data.keys()])}
            WHERE id = %s
        """
        execute_query(doctor_query, list(filtered_data.values()) + [doctor_id])

    # Update doctor assurances
    if "assurances" in profile_data:
        assurances = profile_data["assurances"]

        # Delete existing assurances for the doctor
        delete_assurances_query = "DELETE FROM doctor_assurance WHERE doctor_id = %s"
        execute_query(delete_assurances_query, (doctor_id,))
        # Insert new assurances
        insert_assurances_query = (
            "INSERT INTO doctor_assurance (doctor_id, assurance_id) VALUES (%s, %s)"
        )
        for assurance in assurances:
            # Optionally validate each assurance ID here if needed
            execute_query(
                insert_assurances_query, (doctor_id, assurance["assurance_id"])
            )


def get_all_doctor_information(user_id: int):
    query = """
        SELECT 
            d.*, 
            s.name AS specialization_name,
            TIMESTAMPDIFF(YEAR, experience_start_date, CURDATE()) AS years_of_experience,
            GROUP_CONCAT(a.name) AS assurances
        FROM 
            doctors d
        LEFT JOIN 
            specializations s ON d.specialization_id = s.id
        LEFT JOIN 
            doctor_assurance da ON d.id = da.doctor_id
        LEFT JOIN 
            assurance a ON da.assurance_id = a.id
        WHERE 
            d.id = %s
        GROUP BY 
            d.id
    """
    params = (user_id,)
    doctor = execute_query(query, params, fetch_one=True)
    # Convert assurances from comma-separated string to a list
    if doctor and doctor.get("assurances"):
        doctor["assurances"] = doctor["assurances"].split(",")
    return doctor

def get_doctors(page: int, limit: int):
    offset = (page - 1) * limit
    query = """
        SELECT d.*, s.name AS specialization_name,TIMESTAMPDIFF(YEAR, experience_start_date, CURDATE()) AS years_of_experience,
        GROUP_CONCAT(a.name) AS assurances
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        LEFT JOIN 
            doctor_assurance da ON d.id = da.doctor_id
        LEFT JOIN 
            assurance a ON da.assurance_id = a.id
        GROUP BY d.id
        LIMIT %s OFFSET %s
    """
    doctors = execute_query(query, params=(limit, offset), fetch_all=True)
    if doctors:
        for doctor in doctors:
            if doctor and doctor.get("assurances"):
                doctor["assurances"] = doctor["assurances"].split(",")
    return doctors


def create_specialization(name: str):
    query = "INSERT INTO specializations (name) VALUES (%s)"
    execute_query(query, (name,))
    return {"detail": "Specialization created successfully"}

def get_specializations_from_db():
    query = "SELECT * FROM specializations"
    return execute_query(query, fetch_all=True)
def fetch_assurances():
    query = "SELECT id, name FROM Assurance"
    return execute_query(query, fetch_all=True)
