"""
FastUI support functions
"""
from __future__ import annotations

from typing import List, Optional, Protocol

from loguru import logger
from fastui.events import AnyEvent, BackEvent, GoToEvent
from fastui import AnyComponent, components as c

DFLT_CSS = "text-center py-1 my-1"
DFLT_COL_CSS = f"{DFLT_CSS}"
DFLT_ROW_CSS = f'my-1 border border-bottom border-secondary rounded shadow-sm {DFLT_CSS}'
DFLT_HEAD_CSS = f'my-1 col border {DFLT_CSS}'
DFLT_CONTAINER_CSS = f'{DFLT_CSS}'
DFLT_PAGE_CSS = f'{DFLT_CSS}'


class RowClass(DivPR):

    def __init__(
            self,
            components: List[AnyComponent],
            row_class_name: str = DFLT_ROW_CSS,
            sub_cols=False,
            col_class_name=''
    ):
        row_class_name = f"row {row_class_name}"
        if not components:
            components = [DivPR.empty()]
        if sub_cols:
            components = ColClass.from_list_many(components, class_name=col_class_name)
        super().__init__(components=components, class_name=row_class_name)

    @classmethod
    def from_list_many(cls, components: List[AnyComponent], class_name: str = '') -> List[DivPR]:
        return [cls(components=[comp], row_class_name=class_name) for comp in components]

    @classmethod
    def from_list(cls, components: List[AnyComponent], class_name: str = '') -> DivPR:
        return cls(components=components, row_class_name=class_name)


class ColClass(DivPR):

    def __init__(
            self,
            components: List[AnyComponent],
            col_class: str = DFLT_COL_CSS,
            sub_rows: bool = False,
            row_class: str = DFLT_ROW_CSS
    ):
        col_class = f"col {col_class}"
        if not components:
            components = [DivPR.empty()]
        if sub_rows:
            components = RowClass.from_list_many(components, class_name=row_class)
        super().__init__(components=components, class_name=col_class)

    @classmethod
    def from_list_many(cls, components: List[AnyComponent], class_name: str = DFLT_COL_CSS) -> List[
        ColClass]:
        return [cls(components=[comp], col_class=class_name) for comp in components]

    @classmethod
    def from_list(cls, components: List[AnyComponent], class_name: str = DFLT_COL_CSS) -> DivPR:
        return cls(components=components, col_class=class_name)

    @classmethod
    def empty(cls):
        return cls(components=[DivPR.empty()])


class DivPR(DivPR):
    @classmethod
    def empty(cls):
        return cls(components=[c.Text(text="---")])


class Container(DivPR):
    def __init__(
            self,
            components: List[AnyComponent],
            class_name: str = DFLT_CONTAINER_CSS
    ) -> None:
        class_name = f"container {class_name}"
        super().__init__(components=components, class_name=class_name)

    @classmethod
    def from_list(cls, components: List[AnyComponent], class_name: str = '') -> DivPR:
        return cls(components=components, class_name=class_name)

    @classmethod
    def empty(cls):
        return cls(components=[DivPR.empty()])


class PagePR(c.Page):
    @classmethod
    def default_page(
            cls,
            components: list[AnyComponent],
            title: str = '',
            navbar=None,
            footer=None,
            header_class=DFLT_HEAD_CSS,
            page_classname=DFLT_PAGE_CSS
    ) -> list[AnyComponent]:
        return [
            c.PageTitle(text=f'PawRequest dev - {title}' if title else ''),
            *((navbar,) if navbar else ()),
            c.Page(
                components=[
                    *((c.Heading(text=title, class_name=header_class),) if title else ()),
                    *components,
                ],
                class_name=page_classname,
            ),
            *((footer,) if footer else ()),
        ]

    @classmethod
    def empty_page(cls, nav_bar=None) -> list[AnyComponent]:
        return cls.default_page(
            title="empty page",
            components=[
                c.Heading(text="empty page"),
                DivPR.empty(),
            ],
        )


class LinkPR(c.Link):
    @classmethod
    def custom(cls, title: str, url: str, on_click: Optional[AnyEvent] = None, class_name=""):
        if not url and not on_click:
            logger.error("Must provide url or on_click event")

        on_click = on_click or GoToEvent(url=url)

        return cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)

    @classmethod
    def back(cls) -> c.Link:
        return cls(
            title="Back",
            url="",
            on_click=BackEvent(),
        )

    @classmethod
    def model_nav(cls, model: RoutableModel) -> c.Link:
        return cls(
            components=[c.Text(text=model.__name__.title())],
            on_click=GoToEvent(url=model.rout_prefix()),
            active=f"startswith:{model.rout_prefix()}",
        )


class NavbarPR(c.Navbar):
    @classmethod
    def from_routable(cls, *models: RoutableModel) -> c.Navbar:
        return cls(
            links=[LinkPR.model_nav(_) for _ in models],
        )


class RoutableModel(Protocol):
    """
    RoutableModel has ``rout_prefix`` classmethod
    """

    @classmethod
    def rout_prefix(cls) -> str:
        ...
