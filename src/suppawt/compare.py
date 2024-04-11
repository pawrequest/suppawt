from __future__ import annotations

import typing as _t
import warnings
from typing import Sized

from loguru import logger

T = _t.TypeVar('T', bound='NestedStringSequence')
NestedStrings = type(str | _t.Sequence[T])


def any_in_any(*strings: str | NestedStrings) -> list[str]:
    flattened_strings = set(flatten(strings))
    return [f"'{s1}' matched with '{s2}'"
            for s1 in flattened_strings for s2 in flattened_strings
            if s1.lower() in s2.lower() and s1.lower() != s2.lower()]


def flatten(strings: _t.Sequence[str] | str) -> list[str]:
    for string in strings:
        if isinstance(string, str):
            yield string
        elif isinstance(string, _t.Sequence):
            yield from flatten(string)


def one_in_other(obj: object, obj_var: str, compare_val: str):
    """
     Check if obj has an attribute ``obj_var`` and if that attr's value is in ``compare_val`` or vice-versa.

     :param obj: The object to check.
     :param obj_var: The attribute of obj to check.
     :param compare_val: The value to compare to obj.obj_var.
     :return: True if obj has attr ``obj_var`` and ``compare_val`` is in ``obj_var`` or vice-versa, else False.
     """
    if not hasattr(obj, obj_var):
        logger.warning(f'{obj.__class__.__name__} has no attribute {obj_var}')
        return False
    ob_low = getattr(obj, obj_var).lower()
    return ob_low in compare_val.lower() or compare_val.lower() in ob_low



def instance_log_str(instance: HasTitleOrName) -> str:
    """
    :param instance: The instance to log.
    :return: class name and (title or name) of instance``.
    """
    return f'{instance.__class__.__name__} - {title_or_name_val(instance)}'


def matches_str(matches: Sized, model: type):
    """
    :param matches: A list of model instances.
    :param model: The model class to describe.
    :return: A string describing the number and type of model matches.
    """
    warnings.warn('DEPRICATED use suppawt.compare.matches_str')
    matches = len(matches)
    return f"{matches} '{model.__name__}' {'match' if matches == 1 else 'matches'}"
