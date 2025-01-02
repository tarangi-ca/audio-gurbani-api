from datetime import datetime
from uuid import uuid4

from collection.models import CollectionRecord
from database import database
from pydantic import UUID4


class CollectionRepository:
    async def find(self) -> list[CollectionRecord]:
        async with database.connection() as connection:
            return [
                CollectionRecord.from_row(row)
                for row in await connection.fetch(
                    """
                    SELECT
                        id,
                        display_name,
                        slug,
                        artist_id,
                        created_at,
                        updated_at
                    FROM collections
                    """
                )
            ]

    async def find_by_id(self, id: UUID4) -> CollectionRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    display_name,
                    slug,
                    artist_id,
                    created_at,
                    updated_at
                FROM collections
                WHERE id = $1
                """,
                id,
            )
            return CollectionRecord.from_row(row) if row else None

    async def does_artist_exist(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            return await connection.fetchval(
                "SELECT EXISTS(SELECT 1 FROM artists WHERE id = $1)", id
            )

    async def find_by_artist_id(self, id: UUID4) -> list[CollectionRecord]:
        async with database.connection() as connection:
            return [
                CollectionRecord.from_row(row)
                for row in await connection.fetchmany(
                    """
                    SELECT
                        id,
                        display_name,
                        slug,
                        artist_id,
                        created_at,
                        updated_at
                    FROM collections
                    WHERE artist_id = $1
                    """,
                    id,
                )
            ]

    async def create(
        self, display_name: str, slug: str, artist_id: UUID4
    ) -> CollectionRecord:
        if not await self.does_artist_exist(artist_id):
            raise ValueError("Artist does not exist")

        async with database.connection() as connection:
            return CollectionRecord.from_row(
                await connection.fetchrow(
                    """
                    INSERT INTO collections (id, display_name, slug, artist_id, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $5)
                    RETURNING *
                    """,
                    uuid4(),
                    display_name,
                    slug,
                    artist_id,
                    datetime.now(),
                )
            )

    async def delete(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            result: str = await connection.execute(
                """
                DELETE * FROM collections
                WHERE id = $1
                """,
                id,
            )
            return result.split()[-1] != "0"
