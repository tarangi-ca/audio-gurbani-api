from datetime import datetime

from asyncpg import Record
from collection.models import CollectionRecord
from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class ArtistRecord(CamelCaseBaseModel):
    id: UUID4
    display_name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))


class ArtistWithCollectionsRecord(CamelCaseBaseModel):
    artist: ArtistRecord
    collections: list[CollectionRecord]
