# src/homepage/services.py

from typing import List, Dict
from sqlalchemy.orm import Session
from src.database.connection import create_db_connection
from src.homepage.schemas import DoctorHomepage, SpecialiteResponse

def fetch_specialities(db) -> Dict[int, str]:
    """Fetch all specialities in the database."""
    query = "SELECT id, name FROM specializations"
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        return {row['id']: row['name'] for row in rows}

def fetch_doctors(page: int, db) -> List[DoctorHomepage]:
    """Fetch doctors for the homepage with pagination, including specific attributes."""
    page_size = 6
    offset = (page - 1) * page_size
    query = """
        SELECT 
            d.first_name AS firstname, 
            d.last_name AS familyname, 
            s.name AS specialite, 
            d.state, 
            d.city, 
            d.street, 
            d.photo, 
            d.rating
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        ORDER BY d.first_name, d.last_name
        LIMIT %s OFFSET %s
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        return [DoctorHomepage(**row) for row in rows]

def fetch_doctors_by_specialty(category: str, page: int, db) -> List[DoctorHomepage]:
    """Fetch doctors filtered by category (specialty) with pagination, including specific attributes."""
    page_size = 6
    offset = (page - 1) * page_size
    query = """
        SELECT 
            d.first_name AS firstname, 
            d.last_name AS familyname, 
            s.name AS specialite, 
            d.state, 
            d.city, 
            d.street, 
            d.photo, 
            d.rating
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.id
        WHERE s.name = %s
        ORDER BY d.first_name, d.last_name
        LIMIT %s OFFSET %s
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (category, page_size, offset))
        rows = cursor.fetchall()
        return [DoctorHomepage(**row) for row in rows]






