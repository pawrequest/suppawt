import os

from .backup_paw import Pruner, SQLModelBot, backup_copy_prune
from .error_support import try_except_log_as
from .logger_paw.logger_config_loguru import get_logger
from .async_support import quiet_cancel_as, quiet_cancel_try_log_as, response_
from .misc import hash_simple_md5
from .sqlmodel_support import assign_all, assign_rel, obj_in_session
from .fastui_suport import fuis


def title_or_name_val(obj) -> str:
    return getattr(obj, "title", None) or getattr(obj, "name", None)


def title_or_name_var_val(obj) -> tuple[str, object]:
    var = title_or_name_var(obj)
    return var, getattr(obj, var)


def title_or_name_var(obj) -> str:
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


def param_or_env(env_key: str, value: str | None, none_is_false=False) -> str | bool:
    value = value or os.environ.get(env_key)
    if value is None:
        if none_is_false:
            return False
        raise ValueError(f"{env_key} was not provided and is not an environment variable")

    return value
