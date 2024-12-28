from fastapi import APIRouter, Depends, HTTPException
from src.database.connection import create_db_connection
from src.homepage.schemas import DoctorResponse, CategoryFilterResponse
from src.homepage.services import fetch_doctors, fetch_doctors_by_specialty

router = APIRouter()

@router.get("/homepage", response_model=DoctorResponse)
def get_homepage_doctors(page: int = 1, db=Depends(create_db_connection)):
    """Endpoint to fetch doctors for the homepage."""
    doctors = fetch_doctors(page, db)
    if not doctors:
        raise HTTPException(status_code=404, detail="No more doctors available.")
    return {"doctors": doctors}

@router.get("/homepage/category", response_model=DoctorResponse)
def get_doctors_by_category(category: str, page: int = 1, db=Depends(create_db_connection)):
    """Endpoint to fetch doctors by category."""
    doctors = fetch_doctors_by_specialty(category, page, db)
    if not doctors:
        raise HTTPException(status_code=404, detail="No more doctors available in this category.")
    return {"doctors": doctors}
