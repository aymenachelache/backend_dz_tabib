# src/homepage/schemas.py

from typing import List, Dict, Optional
from pydantic import BaseModel

class SpecialiteResponse(BaseModel):
    specialities: Dict[int, str]

class DoctorHomepage(BaseModel):
    firstname: str
    familyname: str
    specialite: Optional[str]=None
    state: Optional[str]=None
    city: Optional[str]=None
    street: Optional[str]=None
    photo: Optional[str]=None
    rating: Optional[float]=None

class DoctorResponse(BaseModel):
    doctors: List[DoctorHomepage]

class CategoryFilterResponse(BaseModel):
    doctors: List[DoctorHomepage]


