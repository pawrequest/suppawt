import re

"""
functions to convert between different formats
"""


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


def to_snake(s):
    """
    Convert a string to snake_case

    :param s: string to convert
    :return: snake_case string
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
