from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException,BackgroundTasks


from src.auth.services import get_current_user
from src.doctors.services import get_current_doctor
from .schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut, SearcheUserAppointment
from .services import create_appointment, get_day_appointment, searche_patient_appointment, update_appointment
from src.auth.mail import send_email

router = APIRouter()



@router.post("/appointment", response_model=AppointmentOut)
def create_appointment_route(data: AppointmentCreate,background_tasks: BackgroundTasks,user=Depends(get_current_user)):
    appointment = create_appointment(data.dict(),user)
    email_content = f"""
    <h1>Hi {appointment['patient_first_name']}</h1>
    <p>Your <u>{appointment['type']}</u> appointment is scheduled for <u>{appointment['appointment_date']}</u>, don't forget to call us , welcome.</p>
    """
    background_tasks.add_task(send_email,[user.email], "Appointment details",email_content)
    return appointment


@router.put("/appointment/{appointment_id}",response_model=AppointmentOut)
def update_appointment_route(appointment_id: int, data: AppointmentUpdate):
    appointment = update_appointment(appointment_id, data.dict(exclude_unset=True))

    return appointment



@router.get("/appointments/search")
async def search_appointments(first_name: Optional[str]=None, last_name: Optional[str]=None,doctor=Depends(get_current_doctor)):
    appointments =searche_patient_appointment(first_name, last_name,doctor.id)
    return {"appointments": appointments}


@router.get("/appointments/day")
def get_appointments_by_day(
    date: str,
    doctor=Depends(get_current_doctor)  # Fetch the logged-in user
):
    return get_day_appointment(doctor.id,date)

