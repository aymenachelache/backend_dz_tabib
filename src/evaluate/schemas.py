# src/evaluate/schemas.py

from typing import List,Dict
# src/evaluate/schemas.py

from pydantic import BaseModel

class ReviewResponse(BaseModel):
    note: int
    comment: str

class DoctorReviewsResponse(BaseModel):
    reviews: List[ReviewResponse]

class CreateReviewRequest(BaseModel):
    id_doctor: int
    id_patient: int
    note: int
    comment: str

