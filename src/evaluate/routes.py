# src/evaluate/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.connection import create_db_connection
from src.evaluate.schemas import DoctorReviewsResponse, CreateReviewRequest
from src.evaluate.services import fetch_reviews_by_doctor, create_review, calculate_avg_rating,fetch_reviews_by_patient
from src.auth.services import get_current_user
from src.auth.schemas import UserResponse
from typing import List,Dict

router = APIRouter()

@router.get("/evaluate", response_model=DoctorReviewsResponse)
def get_reviews(id_doctor: int):
    """Endpoint to fetch all reviews related to a doctor"""
    reviews = fetch_reviews_by_doctor(id_doctor)
    return {"reviews": reviews}

@router.get("/evaluate/patient", response_model=DoctorReviewsResponse)
def get_reviews(id_patient: int,doctor_id:int):
    """Endpoint to fetch all reviews related to a doctor"""
    reviews = fetch_reviews_by_patient(id_patient,doctor_id)
    return {"reviews": reviews}

@router.post("/evaluate/create")
def post_review(
    request: CreateReviewRequest,
    current_user: UserResponse = Depends(get_current_user)  # Ensure user is authenticated
):
    """Endpoint to create a new review"""
    try:
        create_review(request)
        return {"message": "Review created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/evaluate/calculate_rating")
def calculate_rating(id_doctor: int):
    """Endpoint to calculate and update the average rating for a doctor"""
    try:
        calculate_avg_rating(id_doctor)
        return {"message": "Rating updated successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

