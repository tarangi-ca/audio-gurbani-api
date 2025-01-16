from uuid import uuid4

from pydantic import UUID4, Field
from utilities.schemas import CamelCaseBaseModel


class CreateCollectionBody(CamelCaseBaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    display_name: str
    slug: str
    artist_id: UUID4
