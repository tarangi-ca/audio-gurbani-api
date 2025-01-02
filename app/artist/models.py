from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from asyncpg import Record
from collection.models import CollectionRecord


@dataclass
class ArtistRecord:
    id: uuid4
    display_name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))


@dataclass
class ArtistWithCollectionsRecord:
    artist: ArtistRecord
    collections: list[CollectionRecord]
