from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from hukamnama.models import HukamnamaRecord
from hukamnama.repository import HukamnamaRepository
from pydantic import UUID4

router: APIRouter = APIRouter(prefix="/hukamnamas")


@router.get("/")
async def index(
    repository: Annotated[HukamnamaRepository, Depends()],
) -> list[HukamnamaRecord]:
    return await repository.find()


@router.get("/by-id/{id}")
async def show(
    id: UUID4, repository: Annotated[HukamnamaRepository, Depends()]
) -> HukamnamaRecord | None:
    return await repository.find_by_id(id)


@router.get("/latest")
async def show_latest(
    repository: Annotated[HukamnamaRepository, Depends()],
) -> HukamnamaRecord | None:
    return await repository.find_by_created_at(date.today())


@router.get("/by-created-at/{year}/{month}/{day}")
async def show_by_created_at(
    year: int,
    month: int,
    day: int,
    repository: Annotated[HukamnamaRepository, Depends()],
) -> HukamnamaRecord | None:
    return await repository.find_by_created_at(date(year, month, day))
