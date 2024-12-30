from fastapi import APIRouter, Depends, HTTPException, File, Query, UploadFile,Form
from src.doctors.models import get_specializations_from_db
from src.doctors.schemas import DoctorCreate, DoctorInformation, DoctorProfileUpdate, UserFields
from src.doctors.services import add_profile_photo, fetch_doctors, get_current_doctor, get_doctor_by_id, update_doctor_profile
from src.auth.services import get_current_user
from typing import Annotated, List
from typing import Optional

router = APIRouter()






@router.put("/profile", response_model=DoctorInformation)
def update_profile(profile: DoctorProfileUpdate ,doctor=Depends(get_current_doctor)):
    """API route for updating a doctor's profile."""
    profile_data = profile.dict(exclude_unset=True)

    return update_doctor_profile(doctor.id, profile_data)




@router.get("/doctor", response_model=DoctorInformation)
async def read_doctor(
    current_doctor: Annotated[DoctorInformation, Depends(get_current_doctor)],
):
    return current_doctor

@router.get("/doctors/{doctor_id}", response_model=DoctorInformation)
def get_doctor_information(doctor_id: int):
    return get_doctor_by_id(doctor_id)



@router.get("/doctors", response_model=List[DoctorInformation])
def get_doctors(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """API route to fetch doctors for the homepage."""
    doctors = fetch_doctors(page, limit)
    return doctors




@router.post("/profile/updload", response_model=DoctorInformation)
def add_photo(photo: UploadFile = File(...), user=Depends(get_current_doctor)):
    if not user.is_doctor:
        raise HTTPException(status_code=403, detail="User is not a doctor.")
     
    return add_profile_photo(user.id, photo)


@router.get("/specializations")
def get_specializations():

    return get_specializations_from_db()



