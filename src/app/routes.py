from aiohttp import web

from app.handlers import delete, encode, resolve, stats, update


def setup_routes(app: web.Application) -> None:
    app.router.add_post('/urls', encode)
    app.router.add_get('/urls/{short_code}', resolve)
    app.router.add_get('/urls/{short_code}/stats', stats)
    app.router.add_put('/urls/{short_code}', update)
    app.router.add_delete('/urls/{short_code}', delete)