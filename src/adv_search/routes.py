# src/adv_search/routes.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.database.connection import create_db_connection
from src.adv_search.schemas import AdvancedSearchResponse, DoctorResponse
from src.adv_search.services import fetch_specialities, fetch_assurances, fetch_days_of_week, search_doctors

router = APIRouter()

@router.get("/adv_search", response_model=AdvancedSearchResponse)
def get_adv_search_data(db: Session = Depends(create_db_connection)):
    """Endpoint to fetch all specialities, assurances, and days of the week"""
    specialities = fetch_specialities(db)
    assurances = fetch_assurances(db)
    days_of_week = fetch_days_of_week()
    doctors = []  # Initially no doctors
    return {"specialities": specialities, "assurances": assurances, "days_of_week": days_of_week, "doctors": doctors}

@router.get("/adv_search/search", response_model=DoctorResponse)
def advanced_search(
    specialite: str = Query(None),
    localization: str = Query(None),
    assurance: str = Query(None),
    disponibilite: str = Query(None),
    page: int = Query(1),
    db: Session = Depends(create_db_connection)
):
    """Endpoint to perform advanced search for doctors"""
    criteria = {
        "specialite": specialite,
        "localization": localization,
        "assurance": assurance,
        "disponibilite": disponibilite
    }
    doctors = search_doctors(criteria, page, db)
    return {"doctors": doctors}

