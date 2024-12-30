from typing import Annotated

from banis.schemas import Bani
from banis.service import BaniService
from fastapi import APIRouter, Depends

router: APIRouter = APIRouter()


@router.get("/banis/")
async def index(service: Annotated[BaniService, Depends()]) -> list[Bani]:
    """Get all available banis from the index file.

    Args:
        service (Annotated[BaniService, Depends]): Dependency-injected BaniService instance that handles bani data operations.

    Returns:
        list[Bani]: A list of Bani objects containing bani metadata from the index file.

    Raises:
        HTTPException: 404 if bani index file is not found
        HTTPException: 500 if bani index file cannot be decoded
    """
    return await service.all()
