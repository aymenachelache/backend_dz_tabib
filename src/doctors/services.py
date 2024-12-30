from fastapi import HTTPException, status, Depends, File, UploadFile
import os
from src.auth.schemas import User
from src.auth.services import get_current_doctor_login, get_current_user
from src.doctors.models import (
    get_all_doctor_information,
    get_doctors,
    update_doctor,
)
from src.doctors.schemas import DoctorInformation, DoctorProfileUpdate
from typing import Annotated


UPLOAD_DIR = "uploads/photos/"  # Directory to save photos
DEFAULT_PHOTO = os.path.join(UPLOAD_DIR, "default.png")


def save_photo(photo: UploadFile) -> str:
    # Save the uploaded photo and return its path
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, photo.filename)
    with open(file_path, "wb") as f:
        f.write(photo.file.read())
    return file_path


def add_profile_photo(doctor_id: int, photo: UploadFile):
    photo_path = save_photo(photo)
    update_doctor(doctor_id, {"photo": photo_path})

    doctor_data = get_all_doctor_information(doctor_id)
    if not doctor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor profile not found"
        )
    return DoctorInformation(**doctor_data)



def update_doctor_profile(id: int, profile_data: DoctorProfileUpdate):

    # user_fields = {key: profile_data[key] for key in {"username", "first_name", "last_name", "email"} if key in profile_data}
    doctor_fields = {
        key: profile_data[key]
        for key in {
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "state",
            "city",
            "street",
            "spoken_languages",
            "zoom_link",
            "daily_visit_limit",
            "phone_number",
            "specialization_id",
            "assurances",
            "latitude",
            "longitude",
            "working_days",
        }
        if key in profile_data
    }

    if not doctor_fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Perform the update in the database
    try:
        update_doctor(id, doctor_fields)
        doctor_data = get_all_doctor_information(id)
        if not doctor_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor profile not found"
            )
        return DoctorInformation(**doctor_data)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the doctor profile",
        )


async def get_current_doctor(current_user: Annotated[User, Depends(get_current_doctor_login)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login first"
        )

    doctor = get_all_doctor_information(current_user.id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor profile not found"
        )
    return DoctorInformation(**doctor)


def get_doctor_by_id(id: int):
    if not id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="incorrect id "
        )
    doctor = get_all_doctor_information(id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no doctor with this id"
        )
    return doctor

def fetch_doctors(page: int, limit: int):
    doctors = get_doctors(page, limit)

    if doctors is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no doctors found"
        )
    return doctors
