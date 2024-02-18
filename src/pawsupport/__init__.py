import importlib.util

from . import convert, types_ps


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


if can_import('loguru'):
    from . import logging_ps
    from .types_ps import error_ps
    from . import misc_ps

    if can_import('aiohttp'):
        from . import async_ps

        if can_import('bs4'):
            from . import html_ps

    if can_import('fastui'):
        from . import fastui_ps

    if can_import('context_menu'):
        pass

# internal optional = sqlmodel
from . import backup_ps
