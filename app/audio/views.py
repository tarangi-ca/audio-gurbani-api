from typing import Annotated
from uuid import uuid4

from admin.dependencies import get_current_active_admin
from admin.models import AdminRecord
from audio.models import AudioRecord
from audio.repository import AudioRepository
from audio.schemas import AudioPresignedUrlResponse, CreateAudioRecord
from audio.service import AudioService
from fastapi import APIRouter, Depends
from pydantic import UUID4

router: APIRouter = APIRouter(prefix="/audios")


@router.get("/")
async def index(repository: Annotated[AudioRepository, Depends()]) -> list[AudioRecord]:
    return await repository.find()


@router.get("/{id}")
async def show(
    id: UUID4, repository: Annotated[AudioRepository, Depends()]
) -> AudioRecord | None:
    return await repository.find_by_id(id)


@router.post("/")
async def create(
    body: CreateAudioRecord,
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    repository: Annotated[AudioRepository, Depends()],
) -> AudioRecord:
    return await repository.create(body.id, body.display_name, body.collection_id)


@router.delete("/{id}")
async def delete(
    id: UUID4,
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    repository: Annotated[AudioRepository, Depends()],
) -> bool:
    return await repository.delete(id)


@router.get("/pre-signed-url/{id}")
async def find(
    id: UUID4,
    service: Annotated[AudioService, Depends()],
) -> AudioPresignedUrlResponse:
    return AudioPresignedUrlResponse(
        id=id,
        url=service.find(str(id)),
    )


@router.post("/pre-signed-url")
async def upload(
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    service: Annotated[AudioService, Depends()],
) -> AudioPresignedUrlResponse:
    id: UUID4 = uuid4()
    return AudioPresignedUrlResponse(
        id=id,
        url=service.insert(str(id)),
    )
