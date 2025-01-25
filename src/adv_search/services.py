# src/adv_search/services.py

from typing import List, Dict
from sqlalchemy.orm import Session
from src.adv_search.schemas import DoctorHomepage


def fetch_specialities(db: Session) -> Dict[int, str]:
    query = "SELECT id, name FROM specializations"
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        return {row["id"]: row["name"] for row in rows}


def fetch_assurances(db: Session) -> Dict[int, str]:
    query = "SELECT id , name FROM assurance"
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        return {row["id"]: row["name"] for row in rows}


def fetch_days_of_week() -> List[str]:
    # Hardcode the days of the week
    return [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def search_doctors(
    criteria: Dict[str, str], page: int, db: Session
) -> List[DoctorHomepage]:
    base_query = """
        SELECT DISTINCT
            d.id,
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
        LEFT JOIN Doctor_assurance da ON d.id = da.Doctor_ID
        LEFT JOIN assurance a ON da.assurance_ID = a.id
        LEFT JOIN working_days wd ON d.id = wd.doctor_id
        WHERE 1=1
    """

    conditions = []
    params = []

    if criteria.get("specialite"):
        conditions.append("s.name = %s")
        params.append(criteria["specialite"])

    if criteria.get("localization"):
        loc = criteria["localization"]
        conditions.append("(d.state = %s OR d.city = %s OR d.street = %s)")
        params.extend([loc, loc, loc])

    if criteria.get("assurance"):
        conditions.append("a.Nom_assurance = %s")
        params.append(criteria["assurance"])

    if criteria.get("disponibilite"):
        conditions.append("wd.day_of_week = %s")
        params.append(criteria["disponibilite"])

    if conditions:
        base_query += " AND " + " AND ".join(conditions)

    base_query += " ORDER BY d.first_name, d.last_name LIMIT 6 OFFSET %s"
    params.append((page - 1) * 6)

    with db.cursor(dictionary=True) as cursor:
        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        return [DoctorHomepage(**row) for row in rows]
