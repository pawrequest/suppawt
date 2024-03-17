"""
general purpose functions for suppawt.
"""
from __future__ import annotations

import importlib.util
import os
from typing import Literal, Sized

from loguru import logger

from .get_set import title_or_name_val
from .types import HasTitleOrName


def param_or_env(
        env_key: str, value: str | None, none_is: Literal["fail", "none", "false"] = "fail"
) -> str | bool | None:
    """
    Return ``value``, else ``environment[env_key]``, else ``none_is`` behaviour.

    :param env_key: The environment variable to check.
    :param value: The maybe-value to return if provided.
    :param none_is: If ``value`` and environment[env_key] are both None: "fail" raises ValueError, "none" returns None, "false" returns False.
    :return: ``value`` | ``environment[env_key]`` | ``False`` | ``None`` | *raise*.
    :raises: ValueError if value is None and environment variable env_key is not present and none_is=='fail'.

     """
    value = value or os.environ.get(env_key)
    if value is None:
        if none_is == "none":
            return None
        elif none_is == "false":
            return False
        elif none_is == "fail":
            raise ValueError(f"{env_key} was not provided and is not an environment variable")
        else:
            raise TypeError(f"Invalid value for none_is: {none_is}")

    return value


def one_in_other(obj: object, obj_var: str, compare_val: str):
    """
     Check if obj has an attribute ``obj_var`` and if that attr's value is in ``compare_val`` or vice-versa.

     :param obj: The object to check.
     :param obj_var: The attribute of obj to check.
     :param compare_val: The value to compare to obj.obj_var.
     :return: True if obj has attr ``obj_var`` and ``compare_val`` is in ``obj_var`` or vice-versa, else False.
     """
    if not hasattr(obj, obj_var):
        logger.warning(f"{obj.__class__.__name__} has no attribute {obj_var}")
        return False
    ob_low = getattr(obj, obj_var).lower()
    return ob_low in compare_val.lower() or compare_val.lower() in ob_low


def instance_log_str(instance: HasTitleOrName) -> str:
    """
    :param instance: The instance to log.
    :return: class name and (title or name) of instance``.
    """
    return f"{instance.__class__.__name__} - {title_or_name_val(instance)}"


def matches_str(matches: Sized, model: type):
    """
    :param matches: A list of model instances.
    :param model: The model class to describe.
    :return: A string describing the number and type of model matches.
    """
    matches = len(matches)
    return f"{matches} '{model.__name__}' {'match' if matches == 1 else 'matches'}"


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
