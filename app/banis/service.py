import json
from pathlib import Path

import aiofiles
from banis.schemas import Bani
from fastapi import HTTPException
from settings import settings


class BaniService:
    async def all(self) -> list[Bani]:
        """Retrieve all banis from the index file.

        Loads and parses the banis index JSON file from the configured assets directory.

        Raises:
            HTTPException: 404 if the bani index file cannot be found at the configured path
            HTTPException: 500 if the bani index file cannot be parsed as valid JSON

        Returns:
            list[Bani]: List of Bani objects containing metadata for all available banis
        """
        path: Path = Path(settings.ASSETS_DIRECTORY) / \
            settings.BANIS_INDEX_FILE

        try:
            async with aiofiles.open(path, "r") as file:
                return json.loads(await file.read())["Banis"]
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail=f"Unable to find bani index file at {path}")
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, detail=f"Unable to decode the bani index file at {path}")

    async def compose_audio_path(self, id: str) -> str:
        """Generate the filesystem path for a bani's audio file.

        Args:
            id (str): The unique identifier of the bani

        Raises:
            HTTPException: 404 if no audio file exists for the given bani ID

        Returns:
            str: Full filesystem path to the bani's audio file
        """
        path: Path = Path(settings.ASSETS_DIRECTORY) / \
            id / settings.AUDIO_EXTENSION

        if not path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Audio file not found for bani: {id}"
            )

        return path
