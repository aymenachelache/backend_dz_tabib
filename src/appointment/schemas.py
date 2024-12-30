from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime,date

class AppointmentCreate(BaseModel):
    doctor_id: int
    working_day_id: int
    date: date
    type: Literal['online', 'face_to_face'] = 'face_to_face'
    reason: Optional[str] = None
    status:Literal['pending','cancelled','completed']= 'pending'

class AppointmentUpdate(BaseModel):
    type: Optional[Literal['online', 'face_to_face']]=None
    reason: Optional[str]=None
    status: Optional[str]=None

class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    working_day_id: int
    appointment_date: date
    patient_first_name:Optional[str]
    patient_last_name :Optional[str]
    patient_phone_number: Optional[str]
    type: str
    reason: Optional[str]
    status: str

class SearcheUserAppointment(BaseModel):
    patient_first_name:Optional[str]
    patient_last_name :Optional[str]


