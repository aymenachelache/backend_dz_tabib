


from typing import List
from src.database.query_helper import execute_query


def add_appointment(data,user_id):
    params = (
        data['doctor_id'],
        user_id,
        data['working_day_id'],
        data['date'],
        data.get('reason'),
        data['type'],
    )
    CREATE_APPOINTMENT_QUERY = """
    INSERT INTO appointments (doctor_id, patient_id, working_day_id, appointment_date, reason, type)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(CREATE_APPOINTMENT_QUERY, params, return_last_id=True)


def get_appointment(id):
    query = """
        SELECT 
            a.*, 
            u.first_name as patient_first_name, 
            u.last_name as patient_last_name, 
            u.phone_number  as patient_phone_number
        FROM 
            appointments a
        JOIN 
            users u
        ON 
            a.patient_id = u.id
        WHERE 
            a.id = %s
    """
    params = (id,)
    return execute_query(query, params, fetch_one=True)

def get_day_appointments_number(doctor_id, day_id,date):
    query = "SELECT COUNT(*) as appointment_number FROM appointments WHERE doctor_id = %s AND working_day_id = %s AND appointment_date = %s"
    params = (doctor_id, day_id,date)
    return execute_query(query, params, fetch_one=True)

def user_appoi_number_in_the_day(user_id, day_id,date):
    query = "SELECT COUNT(*) as user_appointment_number FROM appointments WHERE patient_id = %s AND working_day_id = %s AND appointment_date = %s"
    params = (user_id, day_id,date)
    return execute_query(query, params, fetch_one=True)

def update_appointment_attrs(appointment_id, data):
    UPDATE_APPOINTMENT_QUERY = "UPDATE appointments SET {updates} WHERE id = %s"
    updates = ", ".join([f"{key} = %s" for key in data])
    values = list(data.values()) + [appointment_id]
    
    query = UPDATE_APPOINTMENT_QUERY.format(updates=updates)
    rows_affected = execute_query(query, values,check_rows_affected=True)
    return rows_affected

def search_appointments_by_patient_name(first_name: str, last_name: str,doctor_id:int) -> List[dict]:
    query = """
    SELECT appointments.*,users.first_name,users.last_name,users.phone_number
    FROM appointments
    JOIN users ON appointments.patient_id = users.id
    WHERE appointments.doctor_id= %s
    """
    
    query_params = [doctor_id]
    
    # Modify the query and parameters based on the presence of first_name and last_name
    if first_name is not None:
        query += " AND users.first_name LIKE %s"
        query_params.append(f"%{first_name}%")
    
    if last_name is not None:
        query += " AND users.last_name LIKE %s"
        query_params.append(f"%{last_name}%")
    
    query += " ORDER BY appointments.appointment_date ASC"
    # Use your own database execution method here (execute_query is assumed to be a helper function)
    results = execute_query(query, tuple(query_params), fetch_all=True)
    
    return results

def fetch_day_appointment(doctor_id: int, appointment_date: str) -> List[dict]:
    """
    Retrieve all appointments for a specific doctor on a given date.
    """
    query = """
        SELECT 
            appointments.id,
            appointments.appointment_date,
            appointments.reason,
            appointments.type,
            appointments.status,
            patients.first_name AS patient_first_name,
            patients.last_name AS patient_last_name,
            patients.phone_number AS patient_phone_number
        FROM 
            appointments
        JOIN 
            users AS patients ON appointments.patient_id = patients.id
        WHERE 
            appointments.doctor_id = %s AND DATE(appointments.appointment_date) = %s
        ORDER BY 
        appointments.created_at ASC
    """
    params = (doctor_id, appointment_date)
    return execute_query(query, params, fetch_all=True)

