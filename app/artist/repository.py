from datetime import datetime

from artist.models import ArtistRecord, ArtistWithCollectionsRecord
from collection.models import CollectionRecord
from pydantic import UUID4
from utilities.database import database


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
                        description,
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
                    description,
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

    async def create(
        self, id: UUID4, display_name: str, slug: str, description: str | None
    ) -> ArtistRecord:
        async with database.connection() as connection:
            return ArtistRecord.from_row(
                await connection.fetchrow(
                    """
                    INSERT INTO artists (id, display_name, slug, description, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING *
                    """,
                    id,
                    display_name,
                    slug,
                    description,
                    datetime.now(),
                    datetime.now(),
                )
            )

    async def delete(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            result: str = await connection.execute(
                """
                DELETE FROM artists
                WHERE id = $1
                """,
                id,
            )
            return result.split()[-1] != "0"
