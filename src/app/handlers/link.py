import logging

import asyncpg
from aiohttp import web

from app import settings
from app.models import Event, EventType, Link, LinkReport
from app.utils import asdict, get_hash

# Handlers

async def encode(request: web.Request) -> web.Response:
    """ Creates shortened link """
    data = await request.json()
    orig_url = data.get("url")

    logging.error("Trying to encode url: '%s'", orig_url)

    if not Link.is_valid(orig_url):
        logging.error("bad link format")
        return {"error": "bad link format"}, 400

    db_pool: asyncpg.Pool = request.app["db_pool"]

    hashsum: str = get_hash(orig_url)

    created = False

    async with db_pool.acquire() as connection, connection.transaction():
        encoded_link: Link = await Link.get_encoded_link_by_hash(connection, hashsum)

        if not encoded_link:
            encoded_link = await Link.save_encoded_link(connection, orig_url)

    return web.json_response({"data": f"http://{settings.SHORTENER_HOST}/urls/{encoded_link.short_code}"},
                             status=201 if created else 200)


async def resolve(request: web.Request) -> web.Response:
    """ Tries to redirect to original url by its short code """
    short_code: str = request.match_info["short_code"]
    db_pool = request.app["db_pool"]

    async with db_pool.acquire() as connection:
        encoded_link: Link = await Link.get_encoded_link_by_short_code(connection, short_code)

        if not encoded_link:
            return {"error": "link not foound"}, 404
        else:
            await Event.publish(
                connection=connection,
                type=EventType.LINK_RESOLVED,
                payload={
                    "short_code": encoded_link.short_code,
                    "orig_url": encoded_link.orig_url,
                    "link_id": encoded_link.id
                }
            )

    return web.Response(status=302, headers={"Location": encoded_link.orig_url})


async def stats(request: web.Request) -> web.Response:
    """ Gets simple short link stat """
    short_code: str = request.match_info["short_code"]
    db_pool = request.app["db_pool"]

    async with db_pool.acquire() as connection:
        resolve_count = await LinkReport.link_resolve_count_report(
            connection=connection,
            short_code=short_code
        )

    return web.json_response({"data": resolve_count}, status=200)


async def update(request: web.Request) -> web.Response:
    """ Replace original url for shortened link """
    data = await request.json()
    short_code = request.match_info["short_code"]
    orig_url = data.get("url")

    if not Link.is_valid(orig_url):
        return {"error": "bad link format"}, 400

    db_pool = request.app["db_pool"]

    async with db_pool.acquire() as connection, connection.transaction():
        link = await Link.change_orig_url(connection, short_code, orig_url)

        if not link:
            return web.Response(status=404)

    return web.json_response(status=200)


async def delete(request: web.Request) -> web.Response:
    """ Marks shortened link deleted """
    short_code = request.match_info["short_code"]
    db_pool = request.app["db_pool"]

    async with db_pool.acquire() as connection, connection.transaction():
        await Link.delete(connection, short_code)

    return web.json_response(status=200)