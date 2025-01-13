from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class CreateCollectionBody(CamelCaseBaseModel):
    display_name: str
    slug: str
    artist_id: UUID4
