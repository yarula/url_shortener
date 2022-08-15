import logging
from dataclasses import dataclass
from urllib.parse import urlparse

import asyncpg

from app.utils import get_hash


@dataclass
class Link:
    id: str
    hashsum: str
    orig_url: str
    short_code: str

    @staticmethod
    async def get_encoded_link_by_short_code(connection: asyncpg.Connection, short_code: str) -> "Link":
        row = await connection.fetchrow("""
            SELECT id, orig_url, short_code, hashsum
            FROM links
            WHERE short_code = $1
        """, short_code)

        if not row:
            return None

        return Link(**row)


    @staticmethod
    async def get_encoded_link_by_hash(connection: asyncpg.Connection, hashsum: str) -> "Link":
        row = await connection.fetchrow("""
            SELECT
                id,
                hashsum,
                short_code,
                orig_url
            FROM
                links
            WHERE
                hashsum = $1
        """, hashsum)

        if not row:
            return None

        return Link(**row)

    @staticmethod
    async def save_encoded_link(connection: asyncpg.Connection, orig_url: str) -> "Link":
        """ Get random unused permutation to avoid long hashes """

        row = await connection.fetchrow("""
            UPDATE permutations
            SET used = TRUE WHERE value = (
                SELECT value
                FROM permutations
                WHERE used IS FALSE
                ORDER BY random()
                LIMIT 1
            )
            RETURNING value
        """)

        if not row:
            raise RuntimeError("No available suffixes")

        short_code = row["value"]

        row = await connection.fetchrow("""
            INSERT INTO links
            (orig_url, short_code, hashsum)
            VALUES ($1, $2, $3)
            RETURNING id, orig_url, short_code, hashsum
        """, orig_url, short_code, get_hash(orig_url))

        await connection.execute("""
            UPDATE permutations
            SET used = True
            WHERE value = $1
        """, short_code)

        return Link(**row)

    @staticmethod
    async def change_orig_url(connection: asyncpg.connection, short_code: str, new_orig_url: str) -> "Link":
        row = await connection.fetchrow("""
            UPDATE links
            SET orig_url = $2, hashsum = $3
            WHERE short_code = $1
            RETURNING id, short_code, orig_url, hashsum
        """, short_code, new_orig_url, get_hash(new_orig_url))

        if not row:
            return None

        return Link(**row)


    @staticmethod
    async def delete(connection: asyncpg.connection, short_code: str) -> None:
        await connection.execute("""
            UPDATE links 
            SET is_deleted = TRUE 
            WHERE short_code = $1
        """, short_code)


    @staticmethod
    def is_valid(url: str) -> bool:
        try:

            parse_result = urlparse(url)
        except IndexError:
            return False

        return parse_result.netloc and parse_result.scheme