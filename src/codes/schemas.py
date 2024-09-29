from pydantic import BaseModel


class ChangePasswordSchema(BaseModel):
    email: str
    new_password: str
