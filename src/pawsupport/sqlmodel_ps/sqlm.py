from functools import lru_cache
from typing import Sequence

from loguru import logger
from sqlmodel import SQLModel, Session, select

from ..misc_ps import get_hash, instance_log_str, matches_str, one_in_other, snake_name, \
    snake_name_s, title_or_name_val, title_or_name_var
from ..types_ps import HasGetHash, HasTitleOrName


def assign_rel(instance: SQLModel, model: type[SQLModel], matches: list[SQLModel]) -> None:
    if isinstance(instance, model):
        logger.warning(f"Instance is same type as model: {instance.__class__.__name__}")
        return
    try:
        to_extend = getattr(instance, snake_name_s(model))
        to_extend.extend(matches)
    except Exception as e:
        logger.error(f"Error assigning {model.__name__} to {instance.__class__.__name__} - {e}")


async def assign_all(instance: SQLModel, matches_d: dict[str, list[SQLModel]]):
    for group_name, matches in matches_d.items():
        if not matches:
            continue
        model = matches[0].__class__
        assign_rel(instance, model, matches)


def obj_in_session(session, obj: HasGetHash, model: type(SQLModel)) -> bool:
    # todo hash in db
    return get_hash(obj) in [get_hash(_) for _ in session.exec(select(model)).all()]


def db_obj_matches(session: Session, obj: HasTitleOrName, model: type(SQLModel)) -> list[SQLModel]:
    if isinstance(obj, model):
        return []
    db_objs = session.exec(select(model)).all()
    identifier = title_or_name_val(obj)
    obj_var = title_or_name_var(model)

    if matched_tag_models := [_ for _ in db_objs if one_in_other(_, obj_var, identifier)]:
        logger.debug(f"Found {matches_str(matched_tag_models, model)} for {instance_log_str(obj)}")
    return matched_tag_models


async def all_matches(
        session: Session, instance: HasTitleOrName, models: Sequence[SQLModel]
) -> dict[str, list[SQLModel]]:
    res = {
        snake_name_s(model): db_obj_matches(session, instance, model)
        for model in models
    }
    return res


def model_map_(models: Sequence[SQLModel]):
    return {snake_name(_): _ for _ in models}


@lru_cache
def get_other_table_names(obj, data_models) -> list[str]:
    return [snake_name_s(_) for _ in data_models if not isinstance(obj, _)]


@lru_cache
def get_table_names(data_models) -> list[str]:
    return [snake_name_s(_) for _ in data_models]
