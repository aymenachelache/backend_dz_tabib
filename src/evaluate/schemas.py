# src/evaluate/schemas.py

from typing import List,Dict
# src/evaluate/schemas.py

from pydantic import BaseModel

class ReviewResponse(BaseModel):
    patient_id: int
    patient_first_name: str
    patient_last_name: str
    note: int
    comment: str

class DoctorReviewsResponse(BaseModel):
    reviews: List[ReviewResponse]

class CreateReviewRequest(BaseModel):
    id_doctor: int
    id_patient: int
    note: int
    comment: str

