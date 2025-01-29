from datetime import datetime

from asyncpg import Record
from hukamnama.schemas import MehlMapping
from pydantic import UUID4
from utilities.schemas import CamelCaseBaseModel


class HukamnamaRecord(CamelCaseBaseModel):
    id: UUID4
    melody: str
    writer: MehlMapping
    page: int
    text: str
    created_at: datetime

    @classmethod
    def from_row(cls, row: Record):
        content = dict(row)
        if isinstance(content["writer"], str):
            for enum in MehlMapping:
                if enum.value == content["writer"]:
                    content["writer"] = enum
                    break
        return cls(**content)
