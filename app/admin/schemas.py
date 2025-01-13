from utilities.schemas import CamelCaseBaseModel


class CreateAdminBody(CamelCaseBaseModel):
    email_address: str
    password: str
    token: str


class Token(CamelCaseBaseModel):
    access_token: str


class TokenContent(CamelCaseBaseModel):
    id: str | None = None
    email_address: str | None = None
