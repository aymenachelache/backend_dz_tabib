import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
import secrets
from src.auth.models import get_user_by_reset_token

load_dotenv(override=True)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict) -> str:
    """Generate a JWT token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """Verify and decode the JWT token."""
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError :
        raise credentials_exception


def hash_password(password: str) -> str:
    """Hash the password for secure storage."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify if the provided password matches the hashed password."""
    return                 bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))





def generate_reset_token_and_expiry():
    """Generate a secure random token."""
    token=secrets.token_urlsafe(32)
    expiry=expiry = datetime.now() + timedelta(hours=1) 
    return token,expiry


def verify_reset_token(token: str):
    try:
        user=get_user_by_reset_token(token)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        if datetime.now() > user["expiry"]:
            raise HTTPException(status_code=400, detail="Token has expired")
        return user["user_id"]
    except Exception as e:
        raise e

