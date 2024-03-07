import importlib.util

from . import backup_ps, convert, types_ps
from . import logging_ps, misc_ps
from .types_ps import error_ps


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    msg = f'can import: {module_name}' if spec is not None else f'can not import: {module_name}'
    print(msg)
    return spec is not None



if can_import('aiohttp'):
    from . import async_ps

    if can_import('bs4'):
        from . import html_ps

if can_import('context_menu'):
    pass

if can_import('sqlmodel'):
    from .sqlmodel_ps import sqlpr
    if can_import('pytest'):
        from .sqlmodel_ps import sqlpr_test

if can_import('pypdf') and can_import('context-menu'):
    from .pdf_tools import array_pdf

__all__ = [
    'convert',
    'types_ps',
    'logging_ps',
    'error_ps',
    'misc_ps',
    'async_ps',
    'html_ps',
    'backup_ps',
    'sqlpr',
    'sqlpr_test',
    'array_pdf'
]
