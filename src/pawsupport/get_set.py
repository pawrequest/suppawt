import hashlib
import re
from typing import Literal

from pawsupport.convert import to_snake
from .types_ps.typ import HasTitleOrName


def title_or_name_val(obj: HasTitleOrName) -> str:
    res = getattr(obj, "title", None) or getattr(obj, "name", None)
    if not res:
        raise ValueError(f"Can't find title or name on {obj}")
    return res


def title_from_snake(s):
    s = s.replace("_", " ")
    return re.sub(r"(?<!^)(?=[A-Z])", " ", s).title()


def snake_name(obj) -> str:
    return to_snake(obj.__name__).lower()


def snake_name_s(obj) -> str:
    return f"{to_snake(obj.__name__).lower()}s"


def get_hash(obj: object):
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


def hash_simple_md5(data: list):
    return hashlib.md5(",".join(data).encode('utf-8')).hexdigest()


def hash_simple_md5_2(data: list) -> int:
    md5 = hashlib.md5()
    for item in data:
        md5.update(item.encode("utf-8"))
    return int(md5.hexdigest(), 16)


def title_or_name_var_val(obj: HasTitleOrName) -> tuple[str, object]:
    var = title_or_name_var(obj)
    return var, getattr(obj, var)


def title_or_name_var(obj: HasTitleOrName) -> Literal["title", "name"]:
    if hasattr(obj, "title"):
        return "title"
    elif hasattr(obj, "name"):
        return "name"
    else:
        raise TypeError(f"type {type(obj)}")


def slug_or_none(obj) -> str | None:
    return getattr(obj, "slug", None)


def url_slug_or_none(obj):
    return getattr(obj, "url", getattr(obj, "slug", None))
