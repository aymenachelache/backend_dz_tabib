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
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

UPLOAD_DIR = "uploads/photos/"  # Directory to save photos
DEFAULT_PHOTO = os.path.join(UPLOAD_DIR, "default.png")

def upload_photo_to_cloudinary(photo: UploadFile) -> str:
    """Upload a photo to Cloudinary and return the public URL."""
    try:
        # Upload the file to Cloudinary with transformations
        result = cloudinary.uploader.upload(
            photo.file,
            folder="profile_photos",
            transformation=[
                {"width": 200, "height": 200, "crop": "fill"},  # Resize and crop to 200x200
            ],
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload photo: {str(e)}",
        )
    
def delete_photo_from_cloudinary(photo_url: str):
    """Delete a photo from Cloudinary."""
    try:
        # Extract the public ID from the URL
        public_id = photo_url.split("/")[-1].split(".")[0]
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete photo: {str(e)}",
        )

# def save_photo(photo: UploadFile) -> str:
#     # Save the uploaded photo and return its path
#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     file_path = os.path.join(UPLOAD_DIR, photo.filename)
#     with open(file_path, "wb") as f:
#         f.write(photo.file.read())
#     return file_path


def add_profile_photo(doctor_id: int, photo: UploadFile):
    """Add or update a doctor's profile photo using Cloudinary."""
    # Fetch the current doctor data
    doctor_data = get_all_doctor_information(doctor_id)
    if not doctor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor profile not found"
        )

    # Delete the old photo if it exists
    if doctor_data.get("photo"):
        delete_photo_from_cloudinary(doctor_data["photo"])

    # Upload the new photo to Cloudinary
    photo_url = upload_photo_to_cloudinary(photo)

    # Update the doctor's profile with the new photo URL
    doctor_fields = {"photo": photo_url}
    update_doctor(doctor_id, doctor_fields, None, None)

    # Fetch and return the updated doctor data
    updated_doctor_data = get_all_doctor_information(doctor_id)
    return DoctorInformation(**updated_doctor_data)



def update_doctor_profile(doctor_id: int,user_id: int, profile_data: DoctorProfileUpdate):

    user_fields = {key: profile_data[key] for key in {"username", "first_name", "last_name", "email"} if key in profile_data}
    doctor_fields = {
        key: profile_data[key]
        for key in {
            "username",
            "first_name",
            "last_name",
            "email",
            "experience_start_date",
            "state",
            "city",
            "street",
            "spoken_languages",
            "zoom_link",
            "daily_visit_limit",
            "visit_price",
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
        update_doctor(doctor_id, doctor_fields,user_id, user_fields)
        doctor_data = get_all_doctor_information(doctor_id)
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
    if not doctors or doctors[0]["id"]==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no doctors found"
        )
    return doctors
