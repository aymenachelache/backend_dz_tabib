# src/evaluate/services.py

from sqlalchemy.orm import Session
from src.database.query_helper import execute_query
from src.evaluate.schemas import ReviewResponse, CreateReviewRequest
from fastapi import HTTPException
from typing import List, Dict


def fetch_reviews_by_doctor(id_doctor: int) -> List[ReviewResponse]:
    query = """
        SELECT
        u.id as patient_id,
        u.first_name as patient_first_name, u.last_name as patient_last_name,
        r.note, r.comment
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        JOIN users u ON e.patient_id = u.id
        WHERE e.doctor_id = %s AND u.is_doctor = 0
    """
    reviews=execute_query(query, (id_doctor,), fetch_all=True)
    return [ReviewResponse(**review) for review in reviews]



def fetch_reviews_by_patient(id_pat: int,doctor_id : int) -> List[ReviewResponse]:
    query = """
        SELECT r.note, r.comment
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        JOIN users u ON e.patient_id = u.id
        JOIN doctors d ON e.doctor_id = d.id
        WHERE e.patient_id = %s AND u.is_doctor = 0 and e.doctor_id = %s
    """
    reviews=execute_query(query, (id_pat,doctor_id), fetch_all=True)
    return [ReviewResponse(**review) for review in reviews]

# def fetch_reviews_by_patient(id_pat: int) -> List[ReviewResponse]:
#     query = """
#         SELECT r.note, r.comment
#         FROM review r
#         JOIN evaluate e ON r.ID_review = e.review_id
#         JOIN users u ON e.patient_id = u.id
#         WHERE e.patient_id = %s AND u.is_doctor = 0
#     """
#     reviews=execute_query(query, (id_pat,), fetch_all=True)
#     print(reviews)
#     return [ReviewResponse(**review) for review in reviews]


def create_review(request: CreateReviewRequest):

    # Check if id_doctor exists
    doctor =execute_query("SELECT COUNT(*) FROM doctors WHERE id = %s", (request.id_doctor,), fetch_one=True)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")


    # Check if id_patient (now user_id) exists
    patient=execute_query("SELECT COUNT(*) FROM users WHERE id = %s AND is_doctor = 0", (request.id_patient,), fetch_one=True)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient (user) not found")


    result=execute_query("SELECT review_id FROM evaluate WHERE patient_id = %s AND doctor_id = %s", (request.id_patient, request.id_doctor), fetch_one=True) 


    if result:
        # Update existing review
        review_id = result["review_id"]
        update_review_query = """
            UPDATE review SET note = %s, comment = %s WHERE ID_review = %s
        """
        execute_query(update_review_query, (request.note, request.comment, review_id))

    else:
        # Insert new review into the review table
        insert_review_query = """
            INSERT INTO review (note, comment) VALUES (%s, %s)
        """
        review_id = execute_query(insert_review_query, (request.note, request.comment), return_last_id=True)


        # Insert new review into the evaluate table
        insert_evaluate_query = """
            INSERT INTO evaluate (patient_id, doctor_id, review_id) VALUES (%s, %s, %s)
        """
        execute_query(insert_evaluate_query, (request.id_patient, request.id_doctor, review_id))


def calculate_avg_rating(id_doctor: int):


    # Check if id_doctor exists
    doctor=execute_query("SELECT COUNT(*) FROM doctors WHERE id = %s", (id_doctor,), fetch_one=True)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")


    # Calculate the average note
    avg_query = """
        SELECT AVG(r.note) as avg_rating
        FROM review r
        JOIN evaluate e ON r.ID_review = e.review_id
        WHERE e.doctor_id = %s
    """
    avg_rating=execute_query(avg_query, (id_doctor,), fetch_one=True)


    # Update the doctor's rating
    update_query = """
        UPDATE doctors
        SET rating = %s
        WHERE id = %s
    """
    execute_query(update_query, (avg_rating['avg_rating'], id_doctor))

