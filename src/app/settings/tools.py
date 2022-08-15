import os
from typing import TypeVar


class EnvType:
    """
    Available env types.
    """
    testing = 'testing'
    production = 'production'

V = TypeVar('V')


def get_setting(name: str, default: V = None, cast: type = None):
    """
    Get settings from env vars.
    """
    value: V = os.getenv(name)

    if value is None:
        return default

    if default is not None and cast is None:
        cast = type(default)
    elif cast is None:
        cast = str

    if cast is bool:
        return value.lower() in ('yes', 'true', '1')

    return cast(value)
