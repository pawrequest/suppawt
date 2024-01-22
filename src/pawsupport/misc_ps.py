import hashlib
import os
import re
from typing import Literal, Sized

from loguru import logger

from .types_ps import HasTitleOrName


def printel(*els):  # elementtree elements
    print("printel")
    if isinstance(els, str):
        els = [els]
    for el in els:
        print(el)
        for elem in el.iter():
            print(elem.tag, elem.text)


def obj_to_dict(obj: object):
    serializable_types = (int, float, str, bool, type(None))
    return {k: v for k, v in vars(obj).items() if isinstance(v, serializable_types)}


def to_camel(x):
    words = x.split()
    return "".join([words[0].lower()] + [word.capitalize() for word in words[1:]])


def without_keys(d, keys):
    ...
    return {x: d[x] for x in d if x not in keys}


def to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def title_from_snake(s):
    s = s.replace("_", " ")
    return re.sub(r"(?<!^)(?=[A-Z])", " ", s).title()


def snake_name(obj) -> str:
    return to_snake(obj.__name__).lower()


def snake_name_s(obj) -> str:
    return f"{to_snake(obj.__name__).lower()}s"


html_entities = {
    "&": "&amp;",
    "\"": "&quot;",
    "'": "&apos;",
    "<": "&lt;",
    ">": "&gt;",
    " ": "&#32;"
}


def unsanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(entity, char)
    return string


def sanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    return string



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


def title_or_name_val(obj: HasTitleOrName) -> str:
    res = getattr(obj, "title", None) or getattr(obj, "name", None)
    if not res:
        raise ValueError(f"Can't find title or name on {obj}")
    return res


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


def param_or_env(
        env_key: str, value: str | None, none_is: Literal["fail", "none", "false"] = "fail"
) -> str | bool:
    value = value or os.environ.get(env_key)
    if value is None:
        if none_is == "none":
            return None
        elif none_is == "false":
            return False
        elif none_is == "fail":
            raise ValueError(f"{env_key} was not provided and is not an environment variable")
        else:
            raise ValueError(f"Invalid value for none_is: {none_is}")

    return value


def one_in_other(obj: object, obj_var: str, compare_val: str):
    if not hasattr(obj, obj_var):
        logger.warning(f"{obj.__class__.__name__} has no attribute {obj_var}")
        return False
    ob_low = getattr(obj, obj_var).lower()
    return ob_low in compare_val.lower() or compare_val.lower() in ob_low


def instance_log_str(instance: HasTitleOrName):
    return f"{instance.__class__.__name__} - {title_or_name_val(instance)}"


def matches_str(matches: Sized, model: type):
    matches = len(matches)
    return f"{matches} '{model.__name__}' {'match' if matches == 1 else 'matches'}"
