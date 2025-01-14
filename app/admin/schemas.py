from pydantic import BaseModel
from utilities.schemas import CamelCaseBaseModel


class CreateAdminBody(CamelCaseBaseModel):
    email_address: str
    password: str
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenContent(BaseModel):
    id: str | None = None
    email_address: str | None = None
