from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class CreateArtistBody(CamelCaseBaseModel):
    id: UUID4
    display_name: str
    slug: str
    description: str | None
