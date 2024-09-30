from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from src.codes.schemas import ChangePasswordSchema

from src.codes.crud import *


codes_router = APIRouter()


@codes_router.get("/disney/session_code/{email}", tags=["disney_codes"])
def get_code_email(email: str) -> JSONResponse:
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
    try:
        code = get_code_email_by_email(email=email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={
        "code": code,
    }, status_code=status.HTTP_200_OK)


@codes_router.patch("/disney/update_password", tags=["disney_codes"])
def update_password(info: ChangePasswordSchema) -> JSONResponse:
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
    try:
        update_password_by_email(info=info)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={
        "message": "Password updated successfully",
    }, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/temporal_access/{email}", tags=["netflix_codes"])
def get_temporal_access(email: str) -> JSONResponse:

    try:

        code = get_temporal_access_code_by_email(email=email)

        if not code:
            raise HTTPException(status_code=404, detail="Code not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={"code": code}, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/home_code/{email}", tags=["netflix_codes"])
def get_home_code(email: str) -> JSONResponse:

    try:
        message = get_home_code_by_email(email=email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={"content": message}, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/session_code/{email}", tags=["netflix_codes"])
def get_session_code(email: str) -> JSONResponse:

    code = netflix_session_code_by_email(email=email)

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={"code": code}, status_code=status.HTTP_200_OK)
