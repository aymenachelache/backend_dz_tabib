# src/homepage/schemas.py

from typing import List, Dict
from pydantic import BaseModel

class SpecialiteResponse(BaseModel):
    specialities: Dict[int, str]

class DoctorHomepage(BaseModel):
    firstname: str
    familyname: str
    specialite: str
    state: str
    city: str
    street: str
    photo: str
    rating: float

class DoctorResponse(BaseModel):
    doctors: List[DoctorHomepage]

class CategoryFilterResponse(BaseModel):
    doctors: List[DoctorHomepage]


