from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class CreateAudioRecord(CamelCaseBaseModel):
    display_name: str
    collection_id: UUID4


class AudioPresignedUrlResponse(CamelCaseBaseModel):
    id: UUID4
    url: str
