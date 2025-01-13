from datetime import datetime

from asyncpg import Record
from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class CollectionRecord(CamelCaseBaseModel):
    id: UUID4
    display_name: str
    slug: str
    artist_id: UUID4
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))
