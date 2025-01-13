from datetime import datetime

from asyncpg import Record
from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class AdminRecord(CamelCaseBaseModel):
    id: UUID4
    email_address: str
    password: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        return cls(**dict(row))
