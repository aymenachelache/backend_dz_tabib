# src/evaluate/services.py

from sqlalchemy.orm import Session
from src.evaluate.schemas import ReviewResponse, CreateReviewRequest
from fastapi import HTTPException
from typing import List, Dict


def fetch_reviews_by_doctor(id_doctor: int, db: Session) -> List[ReviewResponse]:
    query = """
        SELECT r.note, r.comment
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        JOIN users u ON e.patient_id = u.id
        WHERE e.doctor_id = %s AND u.is_doctor = 0
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (id_doctor,))
        rows = cursor.fetchall()
        return [ReviewResponse(**row) for row in rows]


def fetch_reviews_by_patient(id_pat: int, db: Session) -> List[ReviewResponse]:
    query = """
        SELECT r.note, r.comment
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        JOIN users u ON e.patient_id = u.id
        WHERE e.patient_id = %s AND u.is_doctor = 0
    """
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, (id_pat,))
        rows = cursor.fetchall()
        return [ReviewResponse(**row) for row in rows]


def create_review(request: CreateReviewRequest, db: Session):
    cursor = db.cursor()

    # Check if id_doctor exists
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE id = %s", (request.id_doctor,))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check if id_patient (now user_id) exists
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE id = %s AND is_doctor = 0",
        (request.id_patient,),
    )
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=404, detail="Patient (user) not found")
    # Check if the patient has already evaluated the doctor
    cursor.execute(
        "SELECT review_id FROM evaluate WHERE patient_id = %s AND doctor_id = %s",
        (request.id_patient, request.id_doctor),
    )
    result = cursor.fetchone()

    if result:
        # Update existing review
        review_id = result[0]
        update_review_query = """
            UPDATE review SET note = %s, comment = %s WHERE id = %s
        """
        cursor.execute(update_review_query, (request.note, request.comment, review_id))
        db.commit()
    else:
        # Insert new review into the review table
        insert_review_query = """
            INSERT INTO review (note, comment) VALUES (%s, %s)
        """
        cursor.execute(insert_review_query, (request.note, request.comment))
        db.commit()

        # Get the last inserted review_id
        review_id = cursor.lastrowid

        # Insert into the evaluate table
        insert_evaluate_query = """
            INSERT INTO evaluate (patient_id, doctor_id, review_id) VALUES (%s, %s, %s)
        """
        cursor.execute(
            insert_evaluate_query, (request.id_patient, request.id_doctor, review_id)
        )
        db.commit()

    cursor.close()


def calculate_avg_rating(id_doctor: int, db: Session):
    cursor = db.cursor()

    # Check if id_doctor exists
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE id = %s", (id_doctor,))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Calculate the average note
    avg_query = """
        SELECT AVG(r.note) as avg_rating
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        WHERE e.doctor_id = %s
    """
    cursor.execute(avg_query, (id_doctor,))
    avg_rating = cursor.fetchone()[0]

    # Update the doctor's rating
    update_query = """
        UPDATE doctors
        SET rating = %s
        WHERE id = %s
    """
    cursor.execute(update_query, (avg_rating, id_doctor))
    db.commit()

    cursor.close()
