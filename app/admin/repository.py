from datetime import datetime
from uuid import uuid4

from admin.models import AdminRecord
from passlib.hash import argon2
from pydantic import UUID4
from utilities.database import database


class AdminRepository:
    async def find(self) -> list[AdminRecord]:
        async with database.connection() as connection:
            return [
                AdminRecord.from_row(row)
                for row in await connection.fetch(
                    """
                    SELECT
                        id,
                        email_address,
                        password,
                        created_at,
                        updated_at
                    FROM administrators
                    """
                )
            ]

    async def find_by_id(self, id: UUID4) -> AdminRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    email_address,
                    password,
                    created_at,
                    updated_at
                FROM administrators
                WHERE id = $1
                """,
                id,
            )
            return AdminRecord.from_row(row) if row else None

    async def find_by_email_address(self, email_address: str) -> AdminRecord | None:
        async with database.connection() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    email_address,
                    password,
                    created_at,
                    updated_at
                FROM administrators
                WHERE email_address = $1
                """,
                email_address,
            )
            return AdminRecord.from_row(row) if row else None

    async def create(self, email_address: str, password: str) -> AdminRecord:
        async with database.connection() as connection:
            return AdminRecord.from_row(
                await connection.fetchrow(
                    """
                    INSERT INTO administrators (id, email_address, password, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5)
                    RETURNING *
                    """,
                    uuid4(),
                    email_address,
                    argon2.hash(password),
                    datetime.now(),
                    datetime.now(),
                )
            )

    async def delete(self, id: UUID4) -> bool:
        async with database.connection() as connection:
            result: str = await connection.execute(
                """
                DELETE FROM administrators
                WHERE id = $1
                """,
                id,
            )
            return result.split()[-1] != "0"
