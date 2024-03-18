import math, random
import re

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.auth.utils import decode_jwt
from core.config import settings

from email.message import EmailMessage
import ssl
import smtplib

http_bearer = HTTPBearer()


# checking the jwt token
def check_current_token_auth(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token,)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error {e}")
    return payload


def generate_otp_code(size=6):
    digits = "0123456789"
    otp = ""
    for i in range(size):
        otp += digits[math.floor(random.random() * 10)]
    return otp


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


# mail validation
def check_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def send_email(subject: str, message: str, email_receiver: str):
    email_sender = settings.email_sender
    email_paasword = settings.email_password
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_paasword)
        smtp.sendmail(email_sender, email_receiver, em.as_string())