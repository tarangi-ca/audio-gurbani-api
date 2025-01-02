from pydantic import UUID4, BaseModel


class CreateAdminBody(BaseModel):
    email_address: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenContent(BaseModel):
    id: UUID4 | None = None
    email_address: str | None = None
