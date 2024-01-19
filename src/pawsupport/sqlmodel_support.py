from loguru import logger
from sqlmodel import SQLModel, select

from .misc import to_snake, get_hash


def assign_rel(instance: SQLModel, model: type[SQLModel], matches: list[SQLModel]) -> None:
    if isinstance(instance, model):
        return
    try:
        to_extend = getattr(instance, to_snake(model.__name__ + "s"))
        to_extend.extend(matches)
    except Exception as e:
        logger.error(f"Error assigning {model.__name__} to {instance.__class__.__name__} - {e}")


async def assign_all(instance: SQLModel, matches_d: dict[str, list[SQLModel]]):
    for group_name, matches in matches_d.items():
        if not matches:
            continue
        model = matches[0].__class__
        assign_rel(instance, model, matches)


def obj_in_session(session, obj: SQLModel, model: type(SQLModel)) -> bool:
    # todo hash in db
    return get_hash(obj) in [get_hash(_) for _ in session.exec(select(model)).all()]
