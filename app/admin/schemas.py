from pydantic import BaseModel


class CreateAdminBody(BaseModel):
    email_address: str
    password: str
    token: str


class Token(BaseModel):
    access_token: str


class TokenContent(BaseModel):
    id: str | None = None
    email_address: str | None = None
