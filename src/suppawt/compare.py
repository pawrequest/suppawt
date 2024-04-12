from __future__ import annotations

import typing as _t
import warnings
from collections.abc import Sized

from loguru import logger

type Nested2[T] = T | _t.Collection[Nested2[T]]


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


def flatten_generic[T](invals: Nested2[T]):
    for inval in invals:
        if isinstance(inval, str) or not isinstance(inval, _t.Iterable):
            yield inval
        else:
            yield from flatten_generic(inval)


def handle_match[T](s1: T, s2: T) -> str:
    return f"'{s1}' matched with '{s2}'"


def handle_match_bools[T](s1: T, s2: T) -> bool:
    return s1.lower() in s2.lower() or s2.lower() in s1.lower()


def any_in_any(*invals: Nested2, match_self=False, handler: _t.Callable = handle_match_bools) -> \
        set[str]:
    invals = list(invals)
    wrapper = list if match_self else set
    flattened_invals = wrapper(flatten_generic(invals))
    if len(flattened_invals) < 2:
        raise ValueError(f'Must provide more than one {'' if match_self else 'unique'} string')
    return {
        handler(s1, s2)
        for i1, s1 in enumerate(flattened_invals)
        for i2, s2 in enumerate(flattened_invals)
        if i1 != i2 and s1.lower() in s2.lower()
    }
