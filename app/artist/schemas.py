from pydantic import BaseModel


class CreateArtistBody(BaseModel):
    display_name: str
    slug: str
