from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import get_db

from src.codes.schemas import ChangePasswordSchema

from src.codes.crud import *


codes_router = APIRouter()


@codes_router.get("/disney/session_code/{email}", tags=["disney_codes"])
def get_code_email(email: str, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Retrieve a specific code associated with an email from the database.

    This function queries the database to find a code linked to the provided email. 
    If no code is found, it raises a 404 HTTP exception.

    Args:
        email (str): The email address to search for the associated code.
        db (Session, optional): Database session dependency. Defaults to a FastAPI 
                                dependency injection using `get_db()`.

    Returns:
        JSONResponse: A JSON response containing the code if found, 
                      or a 404 HTTP exception if not found.

    Raises:
        HTTPException: Raised with status code 404 if no code is found for the given email.
    """

    code = get_code_email_by_email(email=email)

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={
        "code": code,
    }, status_code=status.HTTP_200_OK)


@codes_router.patch("/disney/update_password", tags=["disney_codes"])
def update_password(info: ChangePasswordSchema, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Update the password associated with an email in the database.

    This function updates the password associated with the provided email in the database.

    Args:
        email (str): The email address to update the password for.
        password (str): The new password to associate with the email.
        db (Session, optional): Database session dependency. Defaults to a FastAPI 
                                dependency injection using `get_db()`.

    Returns:
        JSONResponse: A JSON response indicating the password was updated successfully.
    """

    update_password_by_email(info=info, db=db)

    return JSONResponse(content={
        "message": "Password updated successfully",
    }, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/temporal_access/{email}", tags=["netflix_codes"])
def get_temporal_access(email: str, db: Session = Depends(get_db)) -> JSONResponse:

    code = get_temporal_access_code_by_email(email=email, db=db)

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={"code": code}, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/home_code/{email}", tags=["netflix_codes"])
def get_home_code(email: str, db: Session = Depends(get_db)) -> JSONResponse:

    message = get_home_code_by_email(email=email, db=db)

    if not message:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={"content": message}, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/session_code/{email}", tags=["netflix_codes"])
def get_session_code(email: str) -> JSONResponse:

    code = netflix_session_code_by_email(email=email)

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={"code": code}, status_code=status.HTTP_200_OK)
