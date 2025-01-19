from typing import Annotated

from admin.dependencies import get_current_active_admin
from admin.models import AdminRecord
from artist.models import ArtistRecord
from artist.repository import ArtistRepository
from artist.schemas import CreateArtistBody
from fastapi import APIRouter, Depends
from pydantic import UUID4

router: APIRouter = APIRouter(prefix="/artists")


@router.get("/")
async def index(
    repository: Annotated[ArtistRepository, Depends()],
) -> list[ArtistRecord]:
    return await repository.find()


@router.get("/{id}")
async def show(
    id: UUID4, repository: Annotated[ArtistRepository, Depends()]
) -> ArtistRecord | None:
    return await repository.find_by_id(id)


@router.post("/")
async def create(
    body: CreateArtistBody,
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    repository: Annotated[ArtistRepository, Depends()],
) -> ArtistRecord:
    return await repository.create(
        body.id, body.display_name, body.slug, body.description
    )


@router.delete("/{id}")
async def delete(
    id: UUID4,
    _: Annotated[AdminRecord, Depends(get_current_active_admin)],
    repository: Annotated[ArtistRepository, Depends()],
) -> bool:
    return await repository.delete(id)
