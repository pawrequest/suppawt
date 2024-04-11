"""
functions for getting and setting attributes on objects.
"""
from __future__ import annotations

import hashlib
import os
from typing import Literal

from . import paw_types
from .paw_types import HasTitleOrName


def title_or_name_val(obj: HasTitleOrName) -> str:
    """
    Get the value of the title or name attribute on an object

    :param obj: object to get title or name from, must have one of those attributes
    :return: value of title or name attribute
    """

    res = getattr(obj, "title", None) or getattr(obj, "name")
    if not res:
        raise ValueError(f"Can't find title or name on {obj}")
    return res


def get_hash(obj: object) -> str:
    """
    Get a hash for an object. If the object has a get_hash method, it will be used. Otherwise, the hash will be
    generated from the object's id, reddit_id, date, title, and name attributes.

    :param obj: object to get hash for
    :return: hash of object
    """
    mapped = []

    if hasattr(obj, "get_hash"):
        if callable(obj.get_hash):
            return obj.get_hash()
        return obj.get_hash

    if hasattr(obj, "id"):
        mapped.append(str(obj.id))

    if hasattr(obj, "reddit_id"):
        mapped.append(obj.reddit_id)

    if hasattr(obj, "date"):
        mapped.append(str(obj.date))

    if hasattr(obj, "title"):
        mapped.append(obj.title)
    if hasattr(obj, "name"):
        mapped.append(obj.name)

    if not mapped:
        raise ValueError(f"Can't find any hashable attributes on {obj}")
    return hash_simple_md5(mapped)


def hash_simple_md5(data: list) -> str:
    """
    Get an md5 hash for a list of strings

    :param data: list of strings to hash
    :return: md5 hash
    """
    return hashlib.md5(",".join(data).encode('utf-8')).hexdigest()


def hash_simple_md5_int(data: list) -> int:
    """
    Get an md5 hash for a list of strings, as an integer

    :param data: list of strings to hash
    :return: md5 hash
    """
    md5 = hashlib.md5()
    for item in data:
        md5.update(item.encode("utf-8"))
    return int(md5.hexdigest(), 16)


def title_or_name_var_val(obj: HasTitleOrName) -> tuple[str, object]:
    """
    Get the name of the title or name attribute on an object, and the value of that attribute

    :param obj: object to get title or name from, must have one of those attributes
    :return: name of title or name attribute, value of title or name attribute
    """
    var = title_or_name_var(obj)
    return var, getattr(obj, var)


def title_or_name_var(obj: HasTitleOrName) -> Literal["title", "name"]:
    """
    Get the name of the title or name attribute on an object (not the value)

    :param obj: object to get title or name from, must have one of those attributes
    :return: 'name' or 'title'
    """
    if hasattr(obj, "title"):
        return "title"
    elif hasattr(obj, "name"):
        return "name"
    else:
        raise TypeError(f"type {type(obj)}")


def slug_or_none(obj) -> str | None:
    """
    Get the slug of an object, or None if it doesn't have one

    :param obj: object to get slug from
    :return: slug of object, or None if it doesn't have one
    """
    return getattr(obj, "slug", None)


def url_slug_or_none(obj) -> str | None:
    """
    Get the url or slug of an object, or None if it doesn't have one

    :param obj: object to get url or slug from
    :return: url or slug of object, or None if it doesn't have one
    """
    return getattr(obj, "url", getattr(obj, "slug", None))


def instance_log_str(instance: paw_types.HasTitleOrName) -> str:
    """
    :param instance: The instance to log.
    :return: class name and (title or name) of instance``.
    """
    return f'{instance.__class__.__name__} - {get_values.title_or_name_val(instance)}'


def param_or_env(
        env_key: str, value: str | None, none_is: Literal['fail', 'none', 'false'] = 'fail'
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
        if none_is == 'none':
            return None
        elif none_is == 'false':
            return False
        elif none_is == 'fail':
            raise ValueError(f'{env_key} was not provided and is not an environment variable')
        else:
            raise TypeError(f'Invalid value for none_is: {none_is}')

    return value
