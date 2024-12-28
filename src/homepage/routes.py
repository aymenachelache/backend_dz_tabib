# src/homepage/routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.database.connection import create_db_connection
from src.homepage.schemas import DoctorResponse, SpecialiteResponse
from src.homepage.services import fetch_doctors, fetch_doctors_by_specialty, fetch_specialities

router = APIRouter()

@router.get("/homepage/specialities", response_model=SpecialiteResponse)
def get_specialities(db=Depends(create_db_connection)):
    """Endpoint to fetch all specialities."""
    specialities = fetch_specialities(db)
    return {"specialities": specialities}

@router.get("/homepage/doctors", response_model=DoctorResponse)
def get_homepage_doctors(category: str = Query("all"), page: int = 1, db=Depends(create_db_connection)):
    """Endpoint to fetch doctors for the homepage based on the provided speciality."""
    if category == "all":
        doctors = fetch_doctors(page, db)
    else:
        doctors = fetch_doctors_by_specialty(category, page, db)
    
    if not doctors:
        raise HTTPException(status_code=404, detail="No more doctors available.")
    return {"doctors": doctors}




