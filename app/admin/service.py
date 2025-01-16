import jwt
from admin.models import AdminRecord
from admin.repository import AdminRepository
from admin.schemas import TokenContent
from passlib.hash import argon2
from utilities.settings import settings


class AdminService:
    def __init__(self):
        self.repository: AdminRepository = AdminRepository()

    def create_access_token(self, content: TokenContent) -> str:
        return jwt.encode(
            content.model_dump(),
            algorithm=settings.JWT_ALGORITHM,
            key=settings.JWT_SECRET_KEY,
        )

    def verify_access_token(self, token: str) -> TokenContent | None:
        try:
            return TokenContent.model_validate(
                jwt.decode(
                    token,
                    key=settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM],
                )
            )
        except jwt.PyJWTError:
            return None

    async def verify_authentication_request(
        self, email_address: str, password: str
    ) -> AdminRecord | None:
        admin: AdminRecord | None = await self.repository.find_by_email_address(
            email_address
        )

        if not admin:
            return None

        if not argon2.verify(password, admin.password):
            return None

        return admin
