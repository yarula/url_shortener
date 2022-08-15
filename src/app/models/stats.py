from datetime import datetime, timedelta

import asyncpg

from .events import EventType


class LinkReport:
    @staticmethod
    async def link_resolve_count_report(connection: asyncpg.Connection, short_code: str, hours: int = 24) -> int:
        link_resolve_count = await connection.fetchval("""
            SELECT
                COUNT(*)
            FROM
                event_log
            WHERE
                type = $1 AND created_at > $2 AND payload->>'short_code' = $3
                
        """, EventType.LINK_RESOLVED.value, datetime.now() - timedelta(hours=hours), short_code)

        return link_resolve_count or 0
