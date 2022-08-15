import logging.config

from aiohttp import web

from app import settings
from app.server import make_server

logger = logging.getLogger(__name__)
logging.config.dictConfig(settings.LOGGING)

app = make_server()

logger.info(
    'Server is starting on %s : %s',
    settings.SERVER_HOST,
    settings.SERVER_PORT,
)

web.run_app(
    app,
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    access_log_format=settings.AIOHTTP_ACCESS_LOG_FORMAT,
)
