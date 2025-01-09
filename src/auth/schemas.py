# auth/schemas.py
from fastapi import Query
from pydantic import BaseModel, ConfigDict,EmailStr,Field, ValidationError
from typing import Annotated,List,Optional
import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., description="Enter a valid phone number.")
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    is_doctor: bool = Field(False)

    class Config:
        allow_population_by_field_name = True



class User(UserRegister):
    id:int
    created_at: datetime.datetime
    disabled: bool = False





class DoctorResponse(BaseModel):
    id: int
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    is_doctor: bool
    created_at: datetime.datetime
    disabled: bool = False

    years_of_experience: Optional[int]=None
    state: Optional[str]=None
    city: Optional[str]=None
    street: Optional[str]=None
    spoken_languages: Optional[str]=None
    zoom_link: Optional[str]=None
    daily_visit_limit: Optional[int]=None
    photo: Optional[str] = None
    phone_number: Optional[str]=None
    specialization : Optional[str]=None
    latitude: Optional[float] =None
    longitude: Optional[float]=None



class UserFromDB(UserRegister):
    id:int
    created_at: datetime.datetime
    disabled: bool = False



class SearchUser(BaseModel):
    username: Optional[str] = None
    email: EmailStr

    

class UserResponse(BaseModel):
    id: int
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    is_doctor: bool
    created_at: datetime.datetime
    disabled: bool = False
    model_config = ConfigDict(from_attributes=True)



class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class EmailModel(BaseModel):
    addresses : List[str]

class Ressetpassword(BaseModel):
    new_password: str
    token:str

class Forgetpassword(BaseModel):
    email: EmailStr




class email(BaseModel):
    email: EmailStr
    
