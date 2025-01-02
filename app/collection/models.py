from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from asyncpg import Record


@dataclass
class CollectionRecord:
    id: uuid4
    display_name: str
    slug: str
    artist_id: uuid4
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))
