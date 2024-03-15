"""
Utility types.
"""
from typing import Protocol, Sequence, runtime_checkable



class Writer(Protocol):
    def write_many(self, content: Sequence = None) -> str:
        ...

    def write_one(self, content=None) -> str:
        ...


class HasGetHash(Protocol):
    """
    Protocol for objects that have a get_hash method
    """

    def get_hash(self) -> int:
        ...


@runtime_checkable
class HasTitle(Protocol):
    title: str


@runtime_checkable
class HasUrl(Protocol):
    url: str


@runtime_checkable
class HasName(Protocol):
    name: str


@runtime_checkable
class HasSlug(Protocol):
    slug: str


HasTitleOrName = HasTitle | HasName
HasSlugOrUrl = HasSlug | HasUrl


def has_title_or_name_and_slug_or_url(obj: HasTitleOrName | HasSlugOrUrl) -> bool:
    """
    Check if an object has both (title or name) and (slug or url) attributes

    :param obj: object to check
    :return: True if object has both (title or name) and (slug or url) attributes, False otherwise
    """
    return isinstance(obj, HasTitleOrName) and isinstance(obj, HasSlugOrUrl)
