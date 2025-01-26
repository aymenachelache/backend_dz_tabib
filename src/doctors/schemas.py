from typing import Optional, List
from pydantic import BaseModel,EmailStr,Field, ValidationError
import datetime



class WorkingHour(BaseModel):
    start_time: str
    end_time: str


class WorkingDay(BaseModel):
    day_of_week: str
    daily_appointment_limit: int
    hours: List[WorkingHour]

class Assurances(BaseModel):
    assurance_id:int
    



class DoctorInformation(BaseModel):
    id : int
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    is_doctor: bool
    created_at: datetime.datetime
    disabled: bool = False
    experience_start_date: Optional[datetime.date]
    years_of_experience: Optional[int]=0
    state: Optional[str]
    city: Optional[str]
    street: Optional[str]
    spoken_languages: Optional[str]
    zoom_link: Optional[str]
    visit_price: Optional[float]
    photo: Optional[str] = None
    phone_number: Optional[str]
    specialization_name : Optional[str]
    specialization_id: Optional[int] = None
    assurances: Optional[List[str]]=None 
    latitude: Optional[float] 
    longitude: Optional[float]
    rating: Optional[float] = 0.0

class DoctorProfileUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    experience_start_date: Optional[datetime.date] = None
    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    spoken_languages: Optional[str] = None
    zoom_link: Optional[str] = None
    visit_price: Optional[float] = None
    phone_number: Optional[str] = None
    specialization_id: Optional[int] = None
    assurances: Optional[List[Assurances]]=None 
    latitude: Optional[float] = None
    longitude: Optional[float] = None

