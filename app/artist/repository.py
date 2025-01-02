from datetime import datetime
from uuid import uuid4

from artist.models import ArtistRecord, ArtistWithCollectionsRecord
from collection.models import CollectionRecord
from database import database
from pydantic import UUID4


class ArtistRepository:
    async def find(self) -> list[ArtistRecord]:
        async with database.connection() as connection:
            return [
                ArtistRecord.from_row(row)
                for row in await connection.fetch(
                    """
                SELECT
                    id,
                    display_name,
                    slug,
                    created_at,
                    updated_at
                FROM artists
                """
                )
            ]

    async def find_by_id(self, id: UUID4) -> ArtistRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    display_name,
                    slug,
                    created_at,
                    updated_at
                FROM artists
                WHERE id = $1
                """,
                id,
            )
            return ArtistRecord.from_row(row) if row else None

    async def find_by_id_with_collections(
        self, id: UUID4
    ) -> ArtistWithCollectionsRecord | None:
        artist: ArtistRecord | None = self.find_by_id(id)

        if not artist:
            return None

        async with database.connection() as connection:
            return ArtistWithCollectionsRecord(
                artist,
                [
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
                ],
            )

    async def create(self, display_name: str, slug: str) -> ArtistRecord:
        async with database.connection() as connection:
            return ArtistRecord.from_row(
                await connection.fetchrow(
                    """
                INSERT INTO artists (id, display_name, slug, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
                """,
                    uuid4(),
                    display_name,
                    slug,
                    datetime.now(),
                    datetime.now(),
                )
            )

    async def delete(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            result: str = await connection.execute(
                """
                DELETE * FROM artists
                WHERE id = $1
                """,
                id,
            )
            return result.split()[-1] != "0"
