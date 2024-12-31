from datetime import timedelta , datetime
from pydantic import BaseModel, Field, root_validator
from typing import Any, List, Optional
import datetime

# Schema for working hours
class WorkingHour(BaseModel):
    hour_id: Optional[int]=None
    start_time:str
    end_time: str

class WorkingHourUpdate(BaseModel):
    hour_id: Optional[int]=None
    start_time:Optional[datetime.time]=None
    end_time: Optional[datetime.time]=None

class CreateHour(BaseModel):
    start_time:datetime.time
    end_time: datetime.time

# Schema for creating a working day with hours
class WorkingDayCreate(BaseModel):
    # doctor_id: int
    day_of_week: str = Field(..., pattern=r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$")
    daily_appointment_limit: int = Field(..., gt=0)
    hours: List[CreateHour]

# Schema for updating a working day
class WorkingDayUpdate(BaseModel):
    daily_appointment_limit: Optional[int] = Field(None, gt=0)
    hours: Optional[List[WorkingHourUpdate]]=None

# Schema for the response of a working day
class WorkingDayResponse(BaseModel):
    day_id: int
    day_of_week: str
    daily_appointment_limit: int
    hours: Optional[List[WorkingHour]] = None


    class Config:
        # Convert timedelta to seconds when returning from the API
        json_encoders = {
            timedelta: lambda v: v.total_seconds()  # Converts timedelta to seconds
        }




