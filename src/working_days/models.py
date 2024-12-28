from fastapi import HTTPException
from src.database.connection import create_db_connection
from src.database.query_helper import execute_query
from src.working_days.schemas import WorkingDayCreate, WorkingDayResponse

# Create a working day
# def create_working_day(doctor_id, day_of_week, daily_appointment_limit):
#     query = """
#     INSERT INTO working_days (doctor_id, day_of_week, daily_appointment_limit)
#     VALUES (%s, %s, %s)
#     """
#     params = (doctor_id, day_of_week, daily_appointment_limit)
#     return execute_query(query, params, return_last_id=True)

# # Create working hours for a working day
# def create_working_hour(working_day_id, start_time, end_time):
#     query = """
#     INSERT INTO working_hours (day_id, start_time, end_time)
#     VALUES (%s, %s, %s)
#     """
#     params = (working_day_id, start_time, end_time)
#     return execute_query(query, params, return_last_id=True)

# # Fetch all working days for a doctor
# def get_working_days(doctor_id):
#     query = """
#     SELECT wd.day_id, wd.day_of_week, wd.daily_appointment_limit, wh.start_time, wh.end_time
#     FROM working_days wd
#     LEFT JOIN working_hours wh ON wd.day_id = wh.day_id
#     WHERE wd.doctor_id = %s
#     """

#     return execute_query(query, (doctor_id,), fetch_all=True)

# def get_working_hours(day_id):
#     query = """
#     SELECT wh.start_time, wh.end_time
#     FROM working_hours wh
#     WHERE wh.day_id = %s
#     """
#     return execute_query(query, (day_id,), fetch_all=True)

# # Update a working day
# def update_working_day(working_day_id, daily_appointment_limit):
#     try:
#         query = """
#         UPDATE working_days
#         SET daily_appointment_limit = %s
#         WHERE day_id = %s
#         """
#         return execute_query(query, (daily_appointment_limit, working_day_id))
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error updating working day")

# def update_working_hour(working_day_id, start_time, end_time):
#     try:
#         query = """
#         UPDATE working_days
#         SET start_time = %s, end_time = %s
#         WHERE day_id = %s
#         """
#         return execute_query(query, (start_time, end_time, working_day_id))
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error updating working day")

# # Delete a working day and its hours
# def delete_working_day(working_day_id):
#     query = "DELETE FROM working_days WHERE id = %s"
#     return execute_query(query, (working_day_id,))

# def delete_working_hour(working_day_id):
#     query = "DELETE FROM working_hours WHERE id = %s"
#     return execute_query(query, (working_day_id,))

# def verify_working_day(doctor_id: int, day_of_week) -> WorkingDayResponse:
#     # Check if the working day already exists
#     query = "SELECT * FROM working_days WHERE doctor_id = %s AND day_of_week = %s"
#     params = (doctor_id,day_of_week)
#     existing_working_day = execute_query(query, params, fetch_all=True)
#     return existing_working_day

# def get_working_day(day_id: int) -> WorkingDayResponse:
#     # Check if the working day already exists
#     query = """
#     SELECT wd.day_id, wd.day_of_week, wd.daily_appointment_limit, wh.start_time, wh.end_time
#     FROM working_days wd
#     LEFT JOIN working_hours wh ON wd.day_id = wh.day_id
#     WHERE wd.day_id = %s
#     """
#     params = (day_id,)
#     existing_working_day = execute_query(query, params, fetch_one=True)
#     return existing_working_day


def create_working_day(doctor_id, day_of_week, daily_appointment_limit):
    query = """
    INSERT INTO working_days (doctor_id, day_of_week, daily_appointment_limit)
    VALUES (%s, %s, %s)
    """
    params = (doctor_id, day_of_week, daily_appointment_limit)
    return execute_query(query, params, return_last_id=True)


# Create working hours for a working day
def create_working_hour(working_day_id, start_time, end_time):
    query = """
    INSERT INTO working_hours (day_id, start_time, end_time)
    VALUES (%s, %s, %s)
    """
    params = (working_day_id, start_time, end_time)
    return execute_query(query, params, return_last_id=True)


# Fetch all working days for a doctor
def get_working_days(doctor_id):
    query = """
    SELECT wd.day_id, wd.day_of_week, wd.daily_appointment_limit
    FROM working_days wd
    WHERE wd.doctor_id = %s
    """

    return execute_query(query, (doctor_id,), fetch_all=True)


def get_working_hours(day_id):
    query = """
    SELECT wh.start_time, wh.end_time, wh.hour_id
    FROM working_hours wh
    WHERE wh.day_id = %s
    """
    return execute_query(query, (day_id,), fetch_all=True)


# Update a working day
def update_working_day(working_day_id, daily_appointment_limit):
    try:
        query = """
        UPDATE working_days
        SET daily_appointment_limit = %s
        WHERE day_id = %s
        """
        return execute_query(query, (daily_appointment_limit, working_day_id))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating working day")


def update_working_hour(working_hour_id, working_day_id, start_time, end_time):
    try:
        query = """
        UPDATE working_hours
        SET start_time = %s, end_time = %s
        WHERE day_id = %s and hour_id = %s
        """
        return execute_query(
            query, (start_time, end_time, working_day_id, working_hour_id)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error updating working day")


# Delete a working day and its hours
def delete_working_day(working_day_id):
    query = "DELETE FROM working_days WHERE day_id = %s"
    return execute_query(query, (working_day_id,))


def delete_working_hour(working_day_id):
    query = "DELETE FROM working_hours WHERE id = %s"
    return execute_query(query, (working_day_id,))


def verify_working_day(doctor_id: int, day_of_week) -> WorkingDayResponse:
    # Check if the working day already exists
    query = "SELECT * FROM working_days WHERE doctor_id = %s AND day_of_week = %s"
    params = (doctor_id, day_of_week)
    existing_working_day = execute_query(query, params, fetch_all=True)
    return existing_working_day


def get_working_day(doctor_id,day_id: int) -> WorkingDayResponse:
    # Check if the working day already exists
    query = """
    SELECT wd.day_id, wd.day_of_week, wd.daily_appointment_limit
    FROM working_days wd
    WHERE wd.day_id = %s and wd.doctor_id = %s
    """
    params = (day_id,doctor_id)
    existing_working_day = execute_query(query, params, fetch_one=True)
    return existing_working_day
