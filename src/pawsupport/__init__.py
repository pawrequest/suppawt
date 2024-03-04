import importlib.util

from . import backup_ps, convert, types_ps
from .pdf_tools.array_pdf import convert_print_silent2


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    msg = f'can import: {module_name}' if spec is not None else f'can not import: {module_name}'
    print(msg)
    return spec is not None


if can_import('loguru'):
    from . import logging_ps, misc_ps
    from .types_ps import error_ps

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

__all__ = [
    'convert',
    'types_ps',
    'convert_print_silent2',
    'logging_ps',
    'error_ps',
    'misc_ps',
    'async_ps',
    'html_ps',
    'backup_ps',
    'sqlpr',
    'sqlpr_test',
]
