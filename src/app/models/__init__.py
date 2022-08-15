import asyncio
import uuid
from typing import Any

import asyncpg
import ujson
from aiohttp import web
from asyncpg.pool import Pool

from .events import Event, EventType
from .links import Link
from .stats import LinkReport


def to_uuid(value: Any) -> uuid.UUID:  # type: ignore
    """UUID type decoder for asyncpg."""
    return uuid.UUID(str(value))


def from_uuid(value: uuid.UUID) -> str:
    """UUID type encoder for asyncpg."""
    return str(value)


async def connection_init(conn: asyncpg.Connection) -> None:
    """Initialize database connection."""
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    await conn.set_type_codec(
        'jsonb',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    await conn.set_type_codec(
        typename='uuid',
        encoder=from_uuid,
        decoder=to_uuid,
        schema='pg_catalog',
    )

async def create_pool(app: web.Application) -> Pool:
    """Create postgres connection pool."""
    settings = app["config"]
    db_pool_settings = {
        'dsn': settings.POSTGRES_DSN,
        'min_size': settings.POSTGRES_POOL_MIN,
        'max_size': settings.POSTGRES_POOL_MAX,
        'init': connection_init,
    }

    pool = await asyncpg.create_pool(**db_pool_settings)
    app['db_pool'] = pool
    return pool


async def close_pool(app: web.Application) -> None:
    """Сlose postgres connection pool."""
    await asyncio.wait_for(app['db_pool'].close(), 10)


def setup_postgres(app: web.Application) -> None:
    app.on_startup.append(create_pool)
    app.on_cleanup.append(close_pool)
