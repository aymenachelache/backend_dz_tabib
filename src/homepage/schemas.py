from pydantic import BaseModel
from typing import List, Optional

class Doctor(BaseModel):
    firstname: str
    familyname: str
    specialty: str
    ville: str
    wilaya: str
    rue: str
    photo_url: Optional[str]
    rating: Optional[float] = 0.0

class DoctorResponse(BaseModel):
    doctors: List[Doctor]

class CategoryFilterResponse(BaseModel):
    doctors: List[Doctor]

