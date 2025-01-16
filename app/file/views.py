from typing import Annotated
from uuid import uuid4

from admin.dependencies import get_current_active_admin
from admin.models import AdminRecord
from fastapi import APIRouter, Depends
from file.schemas import FileFolder, FilePresignedUrlResponse
from file.service import FileService
from pydantic import UUID4

router: APIRouter = APIRouter(prefix="/files")


@router.get("/pre-signed-url/{folder}/{id}")
async def find(
    folder: FileFolder,
    id: UUID4,
    service: Annotated[FileService, Depends()],
) -> FilePresignedUrlResponse:
    return FilePresignedUrlResponse(
        id=id,
        url=service.find(folder, str(id)),
    )


@router.post("/pre-signed-url/{folder}")
async def upload(
    folder: FileFolder,
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    service: Annotated[FileService, Depends()],
) -> FilePresignedUrlResponse:
    id: UUID4 = uuid4()
    return FilePresignedUrlResponse(
        id=id,
        url=service.insert(folder, str(id)),
    )
