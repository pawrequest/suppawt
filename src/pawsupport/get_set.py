import hashlib
import re
from typing import Literal

from pawsupport.convert import to_snake
from .types_ps.typ import HasTitleOrName

""""
functions for getting and setting attributes on objects.
"""


def title_or_name_val(obj: HasTitleOrName) -> str:
    """
    Get the value of the title or name attribute on an object

    :param obj: object to get title or name from, must have one of those attributes
    :return: value of title or name attribute
    """

    res = getattr(obj, "title", None) or getattr(obj, "name", None)
    if not res:
        raise ValueError(f"Can't find title or name on {obj}")
    return res


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
    :return: name of title or name attribute
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
