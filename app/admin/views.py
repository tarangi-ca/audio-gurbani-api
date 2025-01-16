from typing import Annotated

from admin.dependencies import get_current_active_admin
from admin.models import AdminRecord
from admin.repository import AdminRepository
from admin.schemas import CreateAdminBody, Token, TokenContent
from admin.service import AdminService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from utilities.settings import settings

router: APIRouter = APIRouter(prefix="/admins")


@router.get("/")
async def index(
    repository: Annotated[AdminRepository, Depends()],
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
) -> list[AdminRecord]:
    return await repository.find()


@router.get("/{id}")
async def show(
    id: UUID4,
    repository: Annotated[AdminRepository, Depends()],
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
) -> AdminRecord | None:
    return await repository.find_by_id(id)


@router.post("/")
async def create(
    body: CreateAdminBody, repository: Annotated[AdminRepository, Depends()]
) -> AdminRecord:
    if body.token == settings.ADMIN_MASTER_TOKEN:
        return await repository.create(body.email_address, body.password)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate admin master token.",
        )


@router.post("/token")
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AdminService, Depends()],
) -> Token:
    if admin := await service.verify_authentication_request(
        form_data.username, form_data.password
    ):
        return Token(
            access_token=service.create_access_token(
                TokenContent(id=str(admin.id), email_address=admin.email_address)
            ),
            token_type="bearer",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{id}")
async def delete(
    id: UUID4,
    repository: Annotated[AdminRepository, Depends()],
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
) -> bool:
    return await repository.delete(id)
