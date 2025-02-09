from datetime import datetime

from audio.models import AudioRecord
from pydantic import UUID4
from utilities.database import database


class AudioRepository:
    async def find(self) -> list[AudioRecord]:
        async with database.connection() as connection:
            return [
                AudioRecord.from_row(row)
                for row in await connection.fetch(
                    """
                    SELECT
                        id,
                        display_name,
                        collection_id,
                        created_at,
                        updated_at
                    FROM audios
                    """
                )
            ]

    async def find_by_id(self, id: UUID4) -> AudioRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    display_name,
                    collection_id,
                    created_at,
                    updated_at
                FROM audios
                WHERE id = $1
                """,
                id,
            )
            return AudioRecord.from_row(row) if row else None

    async def does_collection_exist(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            return await connection.fetchval(
                "SELECT EXISTS(SELECT 1 FROM collections WHERE id = $1)", id
            )

    async def find_by_collection_id(self, id: UUID4) -> list[AudioRecord]:
        async with database.connection() as connection:
            return [
                AudioRecord.from_row(row)
                for row in await connection.fetch(
                    """
                    SELECT
                        id,
                        display_name,
                        collection_id,
                        created_at,
                        updated_at
                    FROM audios
                    WHERE collection_id = $1
                    """,
                    id,
                )
            ]

    async def create(
        self, id: UUID4, display_name: str, collection_id: UUID4
    ) -> AudioRecord:
        if not await self.does_collection_exist(collection_id):
            raise ValueError("Collection does not exist")

        async with database.connection() as connection:
            return AudioRecord.from_row(
                await connection.fetchrow(
                    """
                    INSERT INTO audios (id, display_name, collection_id, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $4)
                    RETURNING *
                    """,
                    id,
                    display_name,
                    collection_id,
                    datetime.now(),
                )
            )

    async def delete(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            result: str = await connection.execute(
                """
                DELETE FROM audios
                WHERE id = $1
                """,
                id,
            )
            return result.split()[-1] != "0"
