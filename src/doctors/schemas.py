from pydantic import BaseModel
from typing import Optional


class DoctorCreate(BaseModel):
    specialty: str
    clinic_address: Optional[str]
    contact_info: Optional[str]
    certification_documents: Optional[str]
    consultation_fees: Optional[float]


class DoctorUpdate(DoctorCreate):
    pass


class DoctorResponse(BaseModel):
    user_id: int
    specialty: str
    clinic_address: Optional[str]
    contact_info: Optional[str]
    certification_documents: Optional[str]
    consultation_fees: Optional[float]
