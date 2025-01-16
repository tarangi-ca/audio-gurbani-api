from uuid import uuid4

from pydantic import UUID4, Field
from utilities.schemas import CamelCaseBaseModel


class CreateArtistBody(CamelCaseBaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    display_name: str
    slug: str
