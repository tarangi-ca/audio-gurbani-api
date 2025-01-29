from datetime import date
from uuid import uuid4

from hukamnama.models import HukamnamaRecord
from hukamnama.schemas import MehlMapping
from pydantic import UUID4
from utilities.database import database


class HukamnamaRepository:
    async def find(self) -> list[HukamnamaRecord]:
        async with database.connection() as connection:
            return [
                HukamnamaRecord.from_row(row)
                for row in await connection.fetch(
                    """
                    SELECT
                        id,
                        melody,
                        writer,
                        page,
                        text,
                        created_at
                    FROM hukamnamas
                    """
                )
            ]

    async def find_by_id(self, id: UUID4) -> HukamnamaRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    melody,
                    writer,
                    page,
                    text,
                    created_at
                FROM hukamnamas
                WHERE id = $1
                """,
                id,
            )
            return HukamnamaRecord.from_row(row) if row else None

    async def find_by_created_at(self, created_at: date) -> HukamnamaRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    melody,
                    writer,
                    page,
                    text,
                    created_at
                FROM hukamnamas
                WHERE created_at <= $1
                ORDER BY created_at DESC
                LIMIT 1
                """,
                created_at,
            )
            return HukamnamaRecord.from_row(row) if row else None

    async def create(
        self, melody: str, writer: MehlMapping, page: int, text: str
    ) -> HukamnamaRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO hukamnamas (id, melody, writer, page, text)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, melody, writer, page, text, created_at
                """,
                uuid4(),
                melody,
                writer.value,
                page,
                text,
            )
            return HukamnamaRecord.from_row(row) if row else None
