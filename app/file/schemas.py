from enum import Enum

from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class FilePresignedUrlResponse(CamelCaseBaseModel):
    id: UUID4
    url: str


class FileFolder(Enum):
    AUDIO = "audios"
    IMAGE = "images"
