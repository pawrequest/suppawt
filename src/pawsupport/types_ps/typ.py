from dataclasses import dataclass
from typing import Protocol, Sequence, runtime_checkable


class Writer(Protocol):
    def write_many(self, content: Sequence = None) -> str:
        ...

    def write_one(self, content=None) -> str:
        ...


class HasGetHash(Protocol):
    def get_hash(self) -> int:
        ...


@dataclass
class Named:
    name: str


@dataclass
class Titled:
    title: str


@dataclass
class Urled:
    url: str


@dataclass
class Slugged:
    slug: str


@dataclass
class SlugAndName:
    slug: str
    name: str


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
    return isinstance(obj, HasTitleOrName) and isinstance(obj, HasSlugOrUrl)


# HasSlugOrUrlAndNameOrTitle = Union[HasSlugOrUrl, HasTitleOrName]


# named = Named('named')
# titled = Titled('titled')
# urled = Urled('urled')
# slugged = Slugged('slugged')
#
# slug_and_name = SlugAndName('slug', 'name')
#
# assert isinstance(named, HasName)
# assert isinstance(titled, HasTitle)
# assert isinstance(named, HasTitleOrName)
# assert isinstance(titled, HasTitleOrName)
# # assert isinstance(slug_and_name, HasSlugOrUrlAndNameOrTitle)
# ...
# assert has_title_or_name_and_slug_or_url(slug_and_name)
