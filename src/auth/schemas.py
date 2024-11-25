# auth/schemas.py
from fastapi import Query
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,List
import datetime

class UserRegister(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)


class User(UserRegister):
    id:int
    created_at: datetime.datetime
    disabled: bool = False

class SearchUser(BaseModel):
    username: str | None=None
    email: EmailStr

    

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr = Field(...)
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
