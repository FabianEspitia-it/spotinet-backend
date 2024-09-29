import time

from fastapi import HTTPException

from src.utils.disney_methods import get_code_email
from src.utils.disney_methods import introduce_credentials

from src.utils.netflix_methods import *

from src.codes.schemas import ChangePasswordSchema


from sqlalchemy.orm import Session

from src.models import Accounts


def get_code_email_by_email(email: str) -> str:

    time.sleep(5)

    # email_password = db.query(Accounts).filter(
    # Accounts.email == email).first().email_password

    # if not email_password:
    # raise HTTPException(status_code=404, detail="Email not found")

    return get_code_email(user_email=email)


def update_password_by_email(info: ChangePasswordSchema, db: Session) -> None:

    account = db.query(Accounts).filter(
        Accounts.email == info.email).first()

    introduce_credentials(
        user_email=info.email, disney_password=account.disney_password, new_password=info.new_password)

    account.disney_password = info.new_password

    db.commit()

    db.refresh(account)


def get_temporal_access_code_by_email(email: str, db: Session):

    EMAIL_SUBJECT = "Tu código de acceso temporal de Netflix".replace(" ", "")

    time.sleep(6)

    account = db.query(Accounts).filter(Accounts.email == email).first()

    return get_netflix_code_email(user_email=email, netflix_password=account.netflix_password, email_subject=EMAIL_SUBJECT)


def get_home_code_by_email(email: str, db: Session) -> str:

    EMAIL_SUBJECT = "Importante: Cómo actualizar tu Hogar con Netflix".replace(
        " ", "")

    time.sleep(6)

    account = db.query(Accounts).filter(Accounts.email == email).first()

    return get_netflix_code_email(user_email=email, netflix_password=account.netflix_password, email_subject=EMAIL_SUBJECT)


def netflix_session_code_by_email(email: str) -> str:

    time.sleep(7)

    return get_netflix_session_code(user_email=email)
