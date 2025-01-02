from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from asyncpg import Record


@dataclass
class AdminRecord:
    id: uuid4
    email_address: str
    password: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))
