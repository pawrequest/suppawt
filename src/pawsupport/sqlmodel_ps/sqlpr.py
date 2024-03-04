from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache

import sqlalchemy as sqa
from loguru import logger
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

from ..get_set import get_hash, snake_name, snake_name_s, title_or_name_val, title_or_name_var
from ..misc_ps import instance_log_str, matches_str, one_in_other
from ..types_ps import HasTitleOrName
from ..types_ps.typ import HasGetHash


def assign_rel(instance: SQLModel, model: type[SQLModel], matches: list[SQLModel]) -> None:
    """
    Assign a list of models to an instance

    :param instance: instance to assign to
    :param model: model to assign
    :param matches: list of models to assign
    :return: None
    """

    if isinstance(instance, model):
        logger.warning(f'Instance is same type as model: {instance.__class__.__name__}')
        return
    try:
        to_extend = getattr(instance, snake_name_s(model))
        to_extend.extend(matches)
    except Exception as e:
        logger.error(f'Error assigning {model.__name__} to {instance.__class__.__name__} - {e}')


async def assign_all(instance: SQLModel, matches_d: dict[str, list[SQLModel]]) -> None:
    """
    Assign all matches to an instance

    :param instance: instance to assign to
    :param matches_d: dict of matches
    :return: None
    """
    for group_name, matches in matches_d.items():
        if not matches:
            continue
        model = matches[0].__class__
        assign_rel(instance, model, matches)


def obj_in_session(session, obj: HasGetHash, model: type(SQLModel)) -> bool:
    """
    Check if an object is in a session

    :param session: session to check
    :param obj: object to check
    :param model: model to check
    :return: True if object is in session, False otherwise
    """
    # todo hash in db
    return get_hash(obj) in [get_hash(_) for _ in session.exec(select(model)).all()]


def db_obj_matches(session: Session, obj: HasTitleOrName, model: type(SQLModel)) -> list[SQLModel]:
    """
    Get all objects in a session that match an object

    :param session: session to check
    :param obj: object to check
    :param model: model to check
    :return: list of objects that match
    """
    if isinstance(obj, model):
        return []
    db_objs = session.exec(select(model)).all()
    identifier = title_or_name_val(obj)
    obj_var = title_or_name_var(model)

    if matched_tag_models := [_ for _ in db_objs if one_in_other(_, obj_var, identifier)]:
        logger.debug(f'Found {matches_str(matched_tag_models, model)} for {instance_log_str(obj)}')
    return matched_tag_models


async def all_matches(
    session: Session, instance: HasTitleOrName, models: Sequence[SQLModel]
) -> dict[str, list[SQLModel]]:
    """
    Get all matches for an object in a session

    :param session: session to check
    :param instance: object to check
    :param models: models to check
    :return: dict of matches
    """
    res = {snake_name_s(model): db_obj_matches(session, instance, model) for model in models}
    return res


def model_map_(models: Sequence[SQLModel]) -> dict[str, SQLModel]:
    """
    Get a map of model names to models

    :param models: models to map
    :return: dict of model names to models
    """
    return {snake_name(_): _ for _ in models}


@lru_cache
def get_other_table_names(obj, data_models) -> list[str]:
    """
    Get the names of all tables that are not the table of an object

    :param obj: object to check
    :param data_models: models to check
    :return: list of table names
    """
    return [snake_name_s(_) for _ in data_models if not isinstance(obj, _)]


@lru_cache
def get_table_names(data_models) -> list[str]:
    """
    Get the names of all tables

    :param data_models: models to check
    :return: list of table names
    """
    return [snake_name_s(_) for _ in data_models]


class GenericJSONType(sqa.TypeDecorator):
    impl = sqa.JSON

    def __init__(self, model_class: type[BaseModel], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        return value.model_dump_json(round_trip=True) if value is not None else None

    def process_result_value(self, value, dialect):
        return self.model_class.model_validate_json(value) if value else None
