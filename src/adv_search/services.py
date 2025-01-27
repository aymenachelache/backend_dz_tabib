# src/adv_search/services.py

from typing import List, Dict
import pymysql
from sqlalchemy.orm import Session
from src.adv_search.schemas import DoctorHomepage
from src.database.query_helper import execute_query


def fetch_specialities(db: Session) -> Dict[int, str]:
    query = "SELECT id, name FROM specializations"
    rows= execute_query(query,fetch_all=True)
    return rows


def fetch_assurances(db: Session) -> Dict[int, str]:
    query = "SELECT id, name FROM assurance"
    rows= execute_query(query,fetch_all=True)
    print(rows)
    return rows


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
        LEFT JOIN doctor_assurance da ON d.id = da.Doctor_ID
        LEFT JOIN assurance a ON da.assurance_ID = a.id
        LEFT JOIN working_days wd ON d.id = wd.doctor_id
        LEFT JOIN days ON wd.day_id = days.id
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
        conditions.append("a.name = %s")
        params.append(criteria["assurance"])

    if criteria.get("disponibilite"):
        conditions.append("days.day_of_week = %s")
        params.append(criteria["disponibilite"])

    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    print(conditions)
    

    base_query += " ORDER BY d.first_name, d.last_name LIMIT 6 OFFSET %s"
    params.append((page - 1) * 6)
    print(base_query)
    print(params)


    # rows = cursor.fetchall()
    rows= execute_query(base_query,params,fetch_all=True)
    print(rows)
    return rows
