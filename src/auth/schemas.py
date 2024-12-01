# auth/schemas.py
from fastapi import Query
from pydantic import BaseModel,EmailStr,Field, ValidationError
from typing import Annotated,List
import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    phoneNumber: str = Field(..., description="Enter a valid phone number.")
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    is_doctor: bool = Field(False)

    class Config:
        allow_population_by_field_name = True



class User(UserRegister):
    id:int
    created_at: datetime.datetime
    disabled: bool = False





class test(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    password: str
    disabled: bool
    created_at: datetime.datetime
    is_doctor: bool



class UserFromDB(UserRegister):
    id:int
    created_at: datetime.datetime
    disabled: bool = False



class SearchUser(BaseModel):
    username: str | None=None
    email: EmailStr

    

class UserResponse(BaseModel):
    id: int
    username: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    phoneNumber: str = Field(...)
    created_at: datetime.datetime
    disabled: bool = False
    class Config:
        orm_mode = True



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



    
