from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pathlib import Path
from dotenv import load_dotenv
import os
from starlette.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),#os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)


mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message

async def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(recipients, subject, body)
    await mail.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


