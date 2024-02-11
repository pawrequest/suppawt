"""
functions to convert between different formats
"""
from __future__ import annotations

import base64


def obj_to_dict(obj: object) -> dict[str, object]:
    """
    Convert an object's simple attrs to a dictionary

    :param obj: object to convert
    :return: dictionary of object attributes
    """
    serializable_types = (int, float, str, bool, type(None))
    return {k: v for k, v in vars(obj).items() if isinstance(v, serializable_types)}


def to_camel(x) -> str:
    """
    Convert a string to camelCase

    :param x: string to convert
    :return: camelCase string
    """
    words = x.split()
    return "".join([words[0].lower()] + [word.capitalize() for word in words[1:]])


# def to_snake(s):
#     """
#     Convert a string to snake_case
#
#     :param s: string to convert
#     :return: snake_case string
#     """
#     s = s.replace(" ", "_")
#     return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()

def to_snake(s):
    s = ''.join(c.lower() if c.isidentifier() else '_' for c in s)
    return s


def snake_to_pascal(snake_str: str) -> str:
    words = snake_str.split('_')
    return ''.join(word.capitalize() for word in words)


def get_ordinal_suffix(day: int) -> str:
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th') if day not in (11, 12, 13) else 'th'


def base64_encode(data: str) -> str:
    # Encode the data to base64 and then decode it to a string
    return base64.urlsafe_b64encode(data.encode()).decode()


def base64_decode(data: str) -> str:
    # Decode the base64 data back to a string
    return base64.urlsafe_b64decode(data.encode()).decode()
