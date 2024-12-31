



from datetime import date
from typing import List
from src.appointment.model import add_appointment, delete_appointment, fetch_day_appointment, fetch_user_appointment, get_appointment, get_day_appointments_number, search_appointments_by_patient_name, update_appointment_attrs, user_appoi_number_in_the_day
from src.database.query_helper import execute_query
from src.working_days.models import get_working_day
from datetime import datetime
from fastapi import HTTPException, status


def create_appointment(data,user):

    # date_obj = datetime.strptime(data['date'], "%Y-%m-%d")
    day_name = data['date'].strftime("%A")
    # Check working_day
    working_day = get_working_day( data['doctor_id'],data['working_day_id'])

    if not working_day:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid working day for the doctor."
        )
    
    if working_day['day_of_week'] != day_name:
        print(working_day['day_of_week'],day_name)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="the doctor is not working in this date."
        )
    
    if data['date'] < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot book an appointment for a past date."
        )
    
    
    appointment_number=get_day_appointments_number(data['doctor_id'], data['working_day_id'],data['date'])

    if appointment_number['appointment_number'] >= working_day['daily_appointment_limit']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No more appointments available for this working day."
        )
    
    user_appointment_number= user_appoi_number_in_the_day(user.id,data['working_day_id'],data['date'])

    if user_appointment_number['user_appointment_number'] :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You have already book an appointment in this date."
        )
    
    appointment_id = add_appointment(data,user.id)
    appointment=get_appointment(appointment_id)
    return appointment


def update_appointment(appointment_id, data):

    appointment=get_appointment(appointment_id)

    if not appointment :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment not found."
        )
    
    if update_appointment_attrs(appointment_id,data):
        return get_appointment(appointment_id)

    

def searche_patient_appointment(first_name:str, last_name:str,doctor_id:int):
    if not first_name and not last_name :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a fist_name or a last_name or both!"
        )
    return search_appointments_by_patient_name(first_name,last_name,doctor_id)


def get_day_appointment(doctor_id: int, appointment_date: str) -> List[dict]:

    appointments = fetch_day_appointment(doctor_id, appointment_date)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this date.")
    return appointments

def get_user_appointment(user_id: int) -> List[dict]:

    appointments = fetch_user_appointment(user_id)
    filtred_appointments=[]
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found.")
    
    for appointment in appointments:
        if appointment['appointment_date'] >= date.today():
            filtred_appointments.append(appointment)
    return appointments

def remove_appointment(user_id,appointment_id):
    print("2")
    appointment=get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    
    if appointment['patient_id'] != user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to delete this appointment.")
    
    if appointment['appointment_date'] < date.today():
        raise HTTPException(status_code=400, detail="Cannot delete an appointment for a past date.")
    
    if appointment['status'] != 'pending':
        raise HTTPException(status_code=400, detail="Cannot delete an appointment that is not pending.")
    
    print("3")
    appointment_deleted=delete_appointment(user_id,appointment_id)
    if not appointment_deleted:
        raise HTTPException(status_code=500, detail="Error deleting working day") 
    return appointment_deleted




