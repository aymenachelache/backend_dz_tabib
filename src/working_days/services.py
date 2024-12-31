from fastapi import HTTPException
from src.working_days.models import (
    create_working_day,
    create_working_hour,
    get_day_of_week_id,
    get_working_day,
    get_working_days,
    get_working_hours,
    update_working_day,
    delete_working_day,
    update_working_hour,
    verify_working_day
)
from src.working_days.schemas import WorkingDayResponse


def add_working_day_and_hours(doctor_id, day_of_week, daily_appointment_limit, hours):
    day_id_dict = get_day_of_week_id(day_of_week)
    if not day_id_dict:
        raise HTTPException(status_code=400, detail="Invalid day of week")
    
    day_id = day_id_dict["id"]

    if verify_working_day(doctor_id, day_id): 
        raise HTTPException(status_code=400, detail="Working day already exists")
    
    day_created=create_working_day(doctor_id, day_id, daily_appointment_limit)
    if not day_created:
        raise HTTPException(status_code=500, detail="Error creating working day")
    
    for hour in hours:
        hour_created=create_working_hour(day_id,doctor_id, hour.start_time, hour.end_time)
        if not hour_created:
            raise HTTPException(status_code=500, detail="Error creating working hour")
        
    day=get_working_day(doctor_id,day_id)
    hours=get_working_hours(doctor_id,day_id)
    formatted_hours = []
    for hour in hours:
        hour["start_time"] = str(hour["start_time"])
        hour["end_time"] = str(hour["end_time"])
        formatted_hours.append(hour)  # Append the hour to the list of hours
    day["hours"] = formatted_hours
    return day
    # return working_day_id
        


# Service to fetch all working days
def fetch_working_days(doctor_id):
    working_days = get_working_days(doctor_id)
    if not working_days :
        raise HTTPException(status_code=404, detail="No working days found")
    data = []

    for day in working_days:
        hours = get_working_hours(doctor_id,day["day_id"]) 
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
def modify_working_day(doctor_id,day_id, working_hour_id,daily_appointment_limit,hours):
    result=get_working_day(doctor_id,day_id)
    if not result : 
        raise HTTPException(status_code=404, detail="No Working day with this id")
    
    day_updated=update_working_day(doctor_id,day_id, daily_appointment_limit)

    for hour in hours if hours else []:
        hour_updated=update_working_hour(working_hour_id,doctor_id,day_id, hour.start_time,hour.end_time)
        if not hour_updated and not day_updated:
            raise HTTPException(status_code=500, detail="Error updating working day")
        
    day=get_working_day(doctor_id,day_id)
    hours=get_working_hours(doctor_id,day_id)
    formatted_hours = []
    for hour in hours:
        hour["start_time"] = str(hour["start_time"])
        hour["end_time"] = str(hour["end_time"])
        formatted_hours.append(hour)  # Append the hour to the list of hours
    # Create the WorkingDayResponse with the collected hours
    result = WorkingDayResponse(**day, hours=formatted_hours)

    return result

# Service to delete a working day
def remove_working_day(doctor_id,day_id):
    day=get_working_day(doctor_id,day_id)
    if not day:
        raise HTTPException(status_code=404, detail="No Working day with this id")
    
    day_deleted=delete_working_day(doctor_id,day_id)
    if not day_deleted:
        raise HTTPException(status_code=500, detail="Error deleting working day") 
    return day_deleted
