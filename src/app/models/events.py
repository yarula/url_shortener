import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from uuid import uuid4

import asyncpg


class EventType(Enum):
    LINK_RESOLVED = "link_resolved"


@dataclass(frozen=True)
class Event:
    id: str
    type: str
    payload: Dict
    created_at: datetime.datetime

    @staticmethod

    async def publish(connection: asyncpg.Connection, type: EventType, payload: Dict) -> 'Event':
        event_id = uuid4()
        row = await connection.fetchrow("""
           INSERT INTO event_log
           (id, type, payload, created_at)
           VALUES
           ($1, $2, $3, NOW()) 
           RETURNING id, type, payload, created_at
        """, event_id, type.value, payload)

        return Event(**row)