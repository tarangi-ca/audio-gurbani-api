from pydantic import UUID4, BaseModel


class CreateAudioRecord(BaseModel):
    display_name: str
    collection_id: UUID4


class AudioPresignedUrlResponse(BaseModel):
    id: UUID4
    url: str
