from typing import Annotated
from uuid import uuid4

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
async def show(id: UUID4, repository: Annotated[AudioRepository, Depends()]) -> AudioRecord | None:
    return await repository.find_by_id(id)


@router.post("/")
async def create(body: CreateAudioRecord, repository: Annotated[AudioRepository, Depends()]) -> AudioRecord:
    return await repository.create(body.display_name, body.slug, body.artist_id)


@router.delete("/{id}")
async def delete(id: UUID4, repository: Annotated[AudioRepository, Depends()]) -> bool:
    return await repository.delete(id)


@router.get("/pre-signed-url")
async def find(service: Annotated[AudioService, Depends()]) -> AudioPresignedUrlResponse:
    return service.insert(uuid4())


@router.post("/pre-signed-url")
async def upload(service: Annotated[AudioService, Depends()]) -> AudioPresignedUrlResponse:
    return service.insert(uuid4())
