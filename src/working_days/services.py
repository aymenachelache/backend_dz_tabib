from fastapi import HTTPException
from src.working_days.models import (
    create_working_day,
    create_working_hour,
    get_working_day,
    get_working_days,
    get_working_hours,
    update_working_day,
    delete_working_day,
    update_working_hour,
    verify_working_day
)
from src.working_days.schemas import WorkingDayResponse

# Service to create a working day and hours
# def add_working_day_and_hours(doctor_id, day_of_week, daily_appointment_limit, hours):
#     if not verify_working_day(doctor_id, day_of_week):  
#         working_day_id = create_working_day(doctor_id, day_of_week, daily_appointment_limit)
#         for hour in hours:
#             create_working_hour(working_day_id, hour.start_time, hour.end_time)
#         return working_day_id
#     else:
#         raise HTTPException(status_code=400, detail="Working day already exists")


# # Service to fetch all working days
# def fetch_working_days(doctor_id):
#     return get_working_days(doctor_id)

# # Service to update a working day
# def modify_working_day(working_day_id, daily_appointment_limit):
#     result=get_working_day(working_day_id)
#     if result : 
#         update_working_day(working_day_id, daily_appointment_limit)
#     else:
#         raise HTTPException(status_code=404, detail="No Working day with this id")

#     return get_working_day(working_day_id)

# # Service to delete a working day
# def remove_working_day(working_day_id):
#     return delete_working_day(working_day_id)

def add_working_day_and_hours(doctor_id, day_of_week, daily_appointment_limit, hours):
    if not verify_working_day(doctor_id, day_of_week):  
        working_day_id = create_working_day(doctor_id, day_of_week, daily_appointment_limit)
        for hour in hours:
            create_working_hour(working_day_id, hour.start_time, hour.end_time)
        day=get_working_day(working_day_id)
        hours=get_working_hours(working_day_id)
        formatted_hours = []
        for hour in hours:
            hour["start_time"] = str(hour["start_time"])
            hour["end_time"] = str(hour["end_time"])
            formatted_hours.append(hour)  # Append the hour to the list of hours
        day["hours"] = formatted_hours
        return day
        # return working_day_id
    else:
        raise HTTPException(status_code=400, detail="Working day already exists")


# Service to fetch all working days
def fetch_working_days(doctor_id):
    working_days = get_working_days(doctor_id)
    data = []

    for day in working_days:
        hours = get_working_hours(day["day_id"])
        formatted_hours = []  # Initialize a list to collect hours for the day
        for hour in hours:
            hour["start_time"] = str(hour["start_time"])
            hour["end_time"] = str(hour["end_time"])
            formatted_hours.append(hour)  # Append the hour to the list of hours
        
        # Create the WorkingDayResponse with the collected hours
        result = WorkingDayResponse(**day, hours=formatted_hours)
        data.append(result)

    return data


# Service to update a working day
def modify_working_day(working_day_id, working_hour_id,daily_appointment_limit,hours):
    result=get_working_day(working_day_id)
    if result : 
        update_working_day(working_day_id, daily_appointment_limit)
        for hour in hours if hours else []:
            update_working_hour(working_hour_id,working_day_id, hour.start_time,hour.end_time)
    else:
        raise HTTPException(status_code=404, detail="No Working day with this id")
    day=get_working_day(working_day_id)
    hours=get_working_hours(working_day_id)
    formatted_hours = []
    for hour in hours:
        hour["start_time"] = str(hour["start_time"])
        hour["end_time"] = str(hour["end_time"])
        formatted_hours.append(hour)  # Append the hour to the list of hours
    # Create the WorkingDayResponse with the collected hours
    result = WorkingDayResponse(**day, hours=formatted_hours)


    return result

# Service to delete a working day
def remove_working_day(working_day_id):
    return delete_working_day(working_day_id)
