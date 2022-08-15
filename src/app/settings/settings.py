import sys

from aiohttp_apispec import validation_middleware

from .tools import get_setting

AIOHTTP_ACCESS_LOG_FORMAT = '%a %l %u %t "%r" %s %b %Tfsec "%{Referrer}i" "%{User-Agent}i"'

VERSION = 'v1'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'shortener.log',
            'maxBytes': 1024 * 1024 * 100,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'applogfile'],
            'level': 'INFO',
        },
    },
}

DEBUG = True

USE_UVLOOP = True

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

SHORTENER_HOST = 'shrtnr.io'

ENV_TYPE = get_setting('ENV_TYPE', default='localhost')

MIDDLEWARES = [
    validation_middleware,
]

# Database settings
POSTGRES_HOST = get_setting('POSTGRES_HOST', 'shortener.db   ')
POSTGRES_PORT = get_setting('POSTGRES_PORT', '7432')
POSTGRES_DB = get_setting('POSTGRES_DB', 'shortener')
POSTGRES_USER = get_setting('POSTGRES_USER', 'shortener_api')
POSTGRES_PASSWORD = get_setting('POSTGRES_PASSWORD', 'shortener_api')
POSTGRES_POOL_MIN = get_setting('POSTGRES_POOL_MIN', 1)
POSTGRES_POOL_MAX = get_setting('POSTGRES_POOL_MAX', 1)
POSTGRES_DSN = get_setting('POSTGRES_DSN', f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')