from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from settings import settings


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """Initialize the database connection pool"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(settings.DATABASE_URL)

    async def disconnect(self) -> None:
        """Close all database connections"""
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get a database connection from the pool"""
        if self.pool is None:
            raise RuntimeError("Database not connected. Call connect() first")

        async with self.pool.acquire() as connection:
            yield connection


database: Database = Database()
