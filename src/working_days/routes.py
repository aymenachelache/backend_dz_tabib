from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from src.auth.services import get_current_user
from src.doctors.services import get_current_doctor
from src.working_days.models import get_working_day
from src.working_days.schemas import WorkingDayCreate, WorkingDayUpdate, WorkingDayResponse
from src.working_days.services import (
    add_working_day_and_hours,
    fetch_working_days,
    modify_working_day,
    remove_working_day
)

router = APIRouter()

# def convert_seconds_to_time(seconds):
#     hours, remainder = divmod(seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# @router.post("/working-days", response_model=WorkingDayResponse)
# def create_working_day(data: WorkingDayCreate,doctor=Depends(get_current_user)):
#     try:
#         working_day_id = add_working_day_and_hours(
#             doctor.id,
#             data.day_of_week,
#             data.daily_appointment_limit,
#             data.hours
#         )
#         return {"id": working_day_id,"doctor_id":doctor.id,**data.dict()}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error creating working day")

# @router.get("/working-days/{doctor_id}", response_model=List[WorkingDay])
# def get_working_days(doctor_id: int,user=Depends(get_current_user)):
#     try:
#         result=fetch_working_days(doctor_id)
#         for day in result:
#             day["start_time"] = str(day["start_time"])
#             day["end_time"] = str(day["end_time"])
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.put("/working-days/{working_day_id}", response_model=WorkingDay)
# def update_working_day(working_day_id: int, data: WorkingDayUpdate,user=Depends(get_current_user)):

#     result=modify_working_day(working_day_id, data.daily_appointment_limit)
#     result["start_time"] = str(result["start_time"])
#     result["end_time"] = str(result["end_time"])
#     data=WorkingDay(**result)
#     return data


# @router.delete("/working-days/{working_day_id}")
# def delete_working_day(working_day_id: int,doctor=Depends(get_current_user)):
#     try:
#         remove_working_day(working_day_id)
#         return {"message": "Working day deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@router.post("/working-days", response_model=List[WorkingDayResponse])
def create_working_days(data: List[WorkingDayCreate],doctor=Depends(get_current_doctor)):
    response=[]
    try:
        for day in data:
            day = add_working_day_and_hours(
                doctor.id,
                day.day_of_week,
                day.daily_appointment_limit,
                day.hours
            )
            response.append(day)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating working day")

@router.get("/working-days/{doctor_id}", response_model=List[WorkingDayResponse])
def get_working_days(doctor_id: int):
    try:

        result=fetch_working_days(doctor_id)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/working-days/{working_day_id}", response_model=WorkingDayResponse)
def update_working_day(working_day_id: int, data: WorkingDayUpdate,doctor=Depends(get_current_doctor),working_hour_id: Optional[int]=None):
    result=modify_working_day(doctor.id,working_day_id,working_hour_id ,data.daily_appointment_limit,data.hours)
    return result


@router.delete("/working-days/{working_day_id}")
def delete_working_day(working_day_id: int,doctor=Depends(get_current_doctor)):
    try:
        if remove_working_day(doctor.id,working_day_id):
            return {"message": "Working day deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


