# auth/routes.py
from fastapi import APIRouter,status,Depends,BackgroundTasks
from typing import Annotated
from src.auth.schemas import Forgetpassword, User, UserLoginRequest, UserLoginResponse,UserResponse,UserRegister,EmailModel,Ressetpassword, email
from src.auth.services import authenticate_user, create_user,login_for_access_token,get_current_active_user,forgot_password,reset_password
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.mail import send_email


router = APIRouter()


@router.post("/register")
async def register(user: UserRegister,background_tasks: BackgroundTasks ):
    background_tasks.add_task(send_email,[user.email], "Welcome to dz-tabib", "<h1>Welcome to our app</h1>")
    return create_user(user)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],):
    return await login_for_access_token(form_data)


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@router.post("/forgot_password")
async def forgot_password_handler(email: email):
    return await forgot_password(email)

@router.post("/reset_password")
async def reset_password_handler(info: Ressetpassword):
    return await reset_password(info.token, info.new_password)


# @router.post("/login",response_model=UserLoginResponse)
# async def login(user: UserLoginRequest):
#     return await authenticate_user(user.email, user.password)

 