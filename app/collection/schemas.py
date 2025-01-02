from pydantic import UUID4, BaseModel


class CreateCollectionBody(BaseModel):
    display_name: str
    slug: str
    artist_id: UUID4
