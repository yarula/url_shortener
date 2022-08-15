import asyncio
import logging.config

import aiohttp_autoreload
import uvloop
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

from app import settings
from app.models import setup_postgres
from app.routes import setup_routes

logger = logging.getLogger(__name__)

logging.config.dictConfig(settings.LOGGING)


def make_server():
    if settings.DEBUG:
        logger.info('Server restarts on code changes')
        aiohttp_autoreload.start()

    if settings.USE_UVLOOP:
        logger.info('Server uses "UVLOOP" implementation')
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application(middlewares=settings.MIDDLEWARES)

    app["config"] = settings

    setup_routes(app)
    setup_postgres(app)

    setup_aiohttp_apispec(
        app=app,
        title="Demo Url Shortener Documentation",
        version=settings.VERSION,
        url=f'/docs/raw/',
        swagger_path=f'/docs/',
    )

    return app
