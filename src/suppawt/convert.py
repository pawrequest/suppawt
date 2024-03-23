"""FROM PYDANTIC Alias generators for converting between different capitalization conventions."""
from __future__ import annotations

import re
import base64

__all__ = ('to_pascal', 'to_camel', 'to_snake', 'obj_to_dict',
           'get_ordinal_suffix', 'base64_encode', 'base64_decode')


def to_pascal(snake: str) -> str:
    """Convert a snake_case string to PascalCase.

    Args:
        snake: The string to convert.

    Returns:
        The PascalCase string.
    """
    camel = snake.title()
    return re.sub('([0-9A-Za-z])_(?=[0-9A-Z])', lambda m: m.group(1), camel)


def to_camel(snake: str) -> str:
    """Convert a snake_case string to camelCase.

    Args:
        snake: The string to convert.

    Returns:
        The converted camelCase string.
    """
    camel = to_pascal(snake)
    return re.sub('(^_*[A-Z])', lambda m: m.group(1).lower(), camel)


def to_snake(camel: str) -> str:
    """Convert a PascalCase or camelCase string to snake_case.

    Args:
        camel: The string to convert.

    Returns:
        The converted string in snake_case.
    """
    # Handle the sequence of uppercase letters followed by a lowercase letter
    snake = re.sub(r'([A-Z]+)([A-Z][a-z])', lambda m: f'{m.group(1)}_{m.group(2)}', camel)
    # Insert an underscore between a lowercase letter and an uppercase letter
    snake = re.sub(r'([a-z])([A-Z])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
    # Insert an underscore between a digit and an uppercase letter
    snake = re.sub(r'([0-9])([A-Z])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
    # Insert an underscore between a lowercase letter and a digit
    snake = re.sub(r'([a-z])([0-9])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
    return snake.lower()


### CUSTOM FUNCTIONS ###

def obj_to_dict(obj: object) -> dict[str, object]:
    """
    Convert an object's simple attrs to a dictionary

    :param obj: object to convert
    :return: dictionary of object attributes
    """
    serializable_types = (int, float, str, bool, type(None))
    return {k: v for k, v in vars(obj).items() if isinstance(v, serializable_types)}


def get_ordinal_suffix(day: int) -> str:
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th') if day not in (11, 12, 13) else 'th'


def base64_encode(data: str) -> str:
    # Encode the data to base64 and then decode it to a string
    return base64.urlsafe_b64encode(data.encode()).decode()


def base64_decode(data: str) -> str:
    # Decode the base64 data back to a string
    return base64.urlsafe_b64decode(data.encode()).decode()


def title_from_snake(s):
    """
    Convert a snake_case string to a title case string

    :param s: snake_case string
    :return: title case string
    """
    s = s.replace("_", " ")
    return re.sub(r"(?<!^)(?=[A-Z])", " ", s).title()


def snake_name(obj) -> str:
    """
    Get the snake_case name of an object

    :param obj: object to get name from
    :return: snake_case name of object
    """
    return to_snake(obj.__name__).lower()


def snake_name_s(obj) -> str:
    """
    Get the snake_case name of an object, pluralized

    :param obj: object to get name from
    :return: snake_case name of object, pluralized
    """
    return f"{to_snake(obj.__name__).lower()}s"
