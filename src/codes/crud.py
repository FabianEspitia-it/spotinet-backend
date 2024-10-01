import time

from fastapi import HTTPException

from src.utils.disney_methods import get_code_email
from src.utils.disney_methods import introduce_credentials

from src.utils.netflix_methods import *

from src.codes.schemas import ChangePasswordSchema


def get_code_email_by_email(email: str) -> str:

    time.sleep(15)

    # email_password = db.query(Accounts).filter(
    # Accounts.email == email).first().email_password

    # if not email_password:
    # raise HTTPException(status_code=404, detail="Email not found")

    return get_code_email(user_email=email)


def update_password_by_email(info: ChangePasswordSchema) -> None:

    return introduce_credentials(
        user_email=info.email, new_password=info.new_password)


def get_temporal_access_code_by_email(email: str):

    EMAIL_SUBJECT = "Tu código de acceso temporal de Netflix".replace(" ", "")

    time.sleep(8)

    return get_netflix_code_email(user_email=email, email_subject=EMAIL_SUBJECT)


def get_home_code_by_email(email: str) -> str:

    EMAIL_SUBJECT = "Importante:CómoactualizartuHogarconNetflix".replace(
        " ", "")

    time.sleep(8)
    return get_netflix_code_email(user_email=email, email_subject=EMAIL_SUBJECT)


def netflix_session_code_by_email(email: str) -> str:

    time.sleep(7)

    return get_netflix_session_code(user_email=email)
