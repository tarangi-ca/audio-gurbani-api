from typing import Annotated

from admin.models import AdminRecord
from admin.schemas import TokenContent
from admin.service import AdminService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_admin(
    token: Annotated[str, Depends(scheme)], service: Annotated[AdminService, Depends()]
) -> TokenContent | None:
    if content := service.verify_access_token(token):
        admin: AdminRecord | None = await service.repository.find_by_email_address(
            email_address=content.email_address
        )

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return admin


async def get_current_active_admin(
    current_admin: Annotated[TokenContent, Depends(get_current_admin)],
) -> TokenContent:
    return current_admin
