import os
from typing import Literal, Sized

from loguru import logger

from pawsupport.get_set import title_or_name_val


def printel(*els):  # elementtree elements
    print("printel")
    if isinstance(els, str):
        els = [els]
    for el in els:
        print(el)
        for elem in el.iter():
            print(elem.tag, elem.text)


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
