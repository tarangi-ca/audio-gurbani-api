from typing import Annotated

from collection.models import CollectionRecord
from collection.repository import CollectionRepository
from collection.schemas import CreateCollectionBody
from fastapi import APIRouter, Depends
from pydantic import UUID4

router: APIRouter = APIRouter(prefix="/collections")


@router.get("/")
async def index(repository: Annotated[CollectionRepository, Depends()]) -> list[CollectionRecord]:
    return await repository.find()


@router.get("/{id}")
async def show(id: UUID4, repository: Annotated[CollectionRepository, Depends()]) -> CollectionRecord | None:
    return await repository.find_by_id(id)


@router.post("/")
async def create(body: CreateCollectionBody, repository: Annotated[CollectionRepository, Depends()]) -> CollectionRecord:
    return await repository.create(body.display_name, body.slug, body.artist_id)


@router.delete("/{id}")
async def delete(id: UUID4, repository: Annotated[CollectionRepository, Depends()]) -> bool:
    return await repository.delete(id)
