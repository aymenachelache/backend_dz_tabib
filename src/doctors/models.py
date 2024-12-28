from fastapi import HTTPException
from src.database.query_helper import execute_query
from datetime import datetime

from src.doctors.schemas import WorkingDay





# def update_doctor(doctor_id: int, profile_data: dict):
#     # Remove 'working_days' from the profile data to handle separately
#     filtered_data = {key: value for key, value in profile_data.items() if key != 'working_days'}
    
#     if filtered_data:
#         # Prepare and execute the update query for the doctor profile
#         doctor_query = f"""
#             UPDATE doctors
#             SET {', '.join([f"{key} = %s" for key in filtered_data.keys()])}
#             WHERE id = %s
#         """
#         execute_query(doctor_query, list(filtered_data.values()) + [doctor_id])
    

#     return

def update_doctor(doctor_id: int, profile_data: dict):
    filtered_data = {key: value for key, value in profile_data.items() if key != 'working_days'}
    
    if 'specialization_id' in filtered_data:
        specialization_query = "SELECT id FROM specializations WHERE id = %s"
        specialization_exists = execute_query(specialization_query, (filtered_data['specialization_id'],), fetch_one=True)
        if not specialization_exists:
            raise HTTPException(status_code=400, detail="Invalid specialization ID")

    if filtered_data:
        doctor_query = f"""
            UPDATE doctors
            SET {', '.join([f"{key} = %s" for key in filtered_data.keys()])}
            WHERE id = %s
        """
        execute_query(doctor_query, list(filtered_data.values()) + [doctor_id])




# def get_all_doctor_information(user_id:int):
#     query = "SELECT * FROM doctors WHERE doctors.id = %s"
#     params = (user_id,)
#     return execute_query(query, params, fetch_one=True)
def get_all_doctor_information(user_id: int):
    query = """
        SELECT d.*, s.name AS specialization_name 
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        WHERE d.id = %s
    """
    params = (user_id,)
    return execute_query(query, params, fetch_one=True)

def get_doctors(page: int, limit: int):
    offset = (page - 1) * limit
    query = """
        SELECT d.*, s.name AS specialization_name 
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        LIMIT %s OFFSET %s
    """
    return execute_query(query,params=(limit, offset), fetch_all=True)


def create_specialization(name: str):
    query = "INSERT INTO specializations (name) VALUES (%s)"
    execute_query(query, (name,))
    return {"detail": "Specialization created successfully"}

def get_specializations_from_db():
    query = "SELECT * FROM specializations"
    return execute_query(query, fetch_all=True)





        