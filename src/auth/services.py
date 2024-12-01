from fastapi import HTTPException, status,Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from src.auth.utils import  generate_reset_token_and_expiry, hash_password,verify_password,create_access_token,verify_access_token, verify_reset_token
from src.auth.models import get_user_by_email, get_user_by_email_or_username, insert_user, set_reset_token_in_db, update_password
from src.auth.schemas import Forgetpassword, User,UserResponse,TokenData,UserLoginResponse,UserRegister,SearchUser, email
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from src.auth.mail import send_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_user(user:UserRegister):
    # Hash the password
    hashed_password = hash_password(user.password)
    userToSearch=SearchUser(username=user.username,email=user.email)
    
    # Check if the username already exists
    if get_user_by_email_or_username(userToSearch):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already taken"
        )

    try:
        # Insert the user into the database
        user.password = hashed_password
        insert_user(user)
        return {"msg": "User registered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

async def authenticate_user(email: str, password: str):
    """Authenticate user and return an access token if valid."""
    user =  get_user_by_email(email)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify the password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    user_data=user.dict()
    user=UserResponse(**user_data)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)])-> UserResponse: 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception
    user=get_user_by_email(token_data.email)

    if user is None:
        raise credentials_exception
    
    user_data=UserResponse(**(user.dict()))
    return user_data

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def login_for_access_token(form_data: OAuth2PasswordRequestForm) -> UserLoginResponse:

    
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return UserLoginResponse(access_token=access_token, token_type="bearer")




from fastapi.responses import JSONResponse


async def forgot_password(email: email):
    try:
        # Check if the user exists
        user = get_user_by_email(email.email)
        if user is None:
            return JSONResponse(status_code=200, content={"message": "Reset email sent"})

        token,expiry = generate_reset_token_and_expiry()

        # Generate reset token and store in DB
        set_reset_token_in_db(user.id,token,expiry)

        # Construct the reset link
        reset_link = f"http://localhost:5173/reset-password?token={token}"

        # Email content
        subject = "Password Reset Request"
        body = f"""
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>This link expires at {expiry}.</p>
        """

        # Send the email
        await send_email([user.email], subject, body)

        return JSONResponse(status_code=200, content={"message": "Reset email sent"})
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500, content={"error": f"Internal server error"}
        )


async def reset_password(token: str, new_password: str):
    # Verify the token
    user_id = verify_reset_token(token)
    # Hash the new password
    hashed_password = hash_password(new_password)
    update_password(hashed_password, user_id)
    return JSONResponse(status_code=200, content={"message": "Password reset successfully"})


