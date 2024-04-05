from __future__ import annotations

import logging
import sys
from typing import Literal

import loguru
from loguru import logger as logger_

"""
functions for configuring loguru
"""


def get_loguru(
        log_file=None,
        profile: Literal['local', 'remote', 'default'] = 'local',
        category_dict: dict | None = None
) -> logger_:
    if profile == 'local':
        logger_.info('Using local log profile')
        terminal_format = log_fmt_local_terminal
    elif profile == 'remote':
        logger_.info('Using remote log profile')
        terminal_format = log_fmt_server_terminal
    else:
        raise ValueError(f'Invalid profile: {profile}')

    logger_.remove()
    if log_file:
        logger_.add(log_file, rotation='1 day', delay=True, encoding='utf8')

    logger_.add(sys.stderr, level='DEBUG', format=terminal_format)

    return logger_


CAT_COLOR = {
    'episode': 'cyan',
    'reddit': 'green',
    'backup': 'magenta',
}


def log_fmt_local_terminal(record: loguru.Record) -> str:
    file_txt = f"{record['file'].path}:{record['line']}"

    category = record['extra'].get('category', 'General')
    category_txt = f'{category.title():<9}'

    color = CAT_COLOR.get(category.lower(), 'white')
    category_txt = f'| {coloured(category_txt, color)}' if category_txt != 'General' else ''
    lvltext = f'<lvl>{record['level']: <7}</lvl>'
    msg_txt = f'<lvl>{record['message']}</lvl>'
    # msg_txt = f'{record['message']}'
    return f"{lvltext} {category_txt} | {msg_txt} | {file_txt}\n"


def get_terminal_format():
    return log_fmt_local_terminal


def coloured(msg: str, colour: str) -> str:
    """
    Colour a message

    :param msg: message to colour
    :param colour: colour to use
    :return: coloured message
    """
    return f'<{colour}>{msg}</{colour}>'


def log_fmt_server_terminal(record: logging.LogRecord) -> str:
    """
    Format for server-side logging

    :param record: log record
    :return: formatted log record
    """
    category = record['extra'].get('category', 'General')
    category = f'{category:<9}'
    colour = CAT_COLOR.get(category, 'white')

    file_line = f"{record['file']}:{record['line']}- {record['function']}()"
    bot_says = f"<bold>{coloured(category, colour):<9} </bold> | <lvl>{record['message']}</lvl>"

    return f"<lvl>{record['level']: <7} </lvl>| {bot_says} | {file_line}\n"


logger = get_loguru(profile="local")
