"""
FastUI support functions
"""
from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Protocol

from loguru import logger
from fastui.events import AnyEvent, BackEvent, GoToEvent
from fastui import AnyComponent, components as c

_DFLT_CSS_STR = "text-center py-1 my-1"


class CSSEnum:
    LINK = ''
    PLAIN = "text-center py-1 my-1"
    COL = f"{PLAIN}"
    ROW = f'my-1 border border-bottom border-secondary rounded shadow-sm {PLAIN}'
    HEAD = f'my-1 col border {PLAIN}'
    CONTAINER = f'{PLAIN}'
    PAGE = f'{PLAIN}'

    HEAD_DIV = f"{PLAIN}"
    HEAD_ROW = f"my-1 col border {PLAIN}"
    TITLE_COL = f"col-4 {PLAIN}"
    SUB_LIST = f"{PLAIN}"


class LayoutMode(Enum):
    SINGLE = auto()  # All components in a single row/col
    MULTIPLE = auto()  # Each component in its own row/col
    NESTED = auto()  # Each component in its own row/col, all nested in another row/col


class WrapMode(Enum):
    SAME = auto()
    OTHER = auto()


class DivPR(c.Div):
    def __init__(
            self,
            components: list[AnyComponent],
            class_name: str = CSSEnum.PLAIN,
            layout_mode: LayoutMode = LayoutMode.SINGLE,
            wrap_in: Optional[type[Row] | type[Col]] = None,
            wrap_mode: WrapMode = WrapMode.OTHER
    ):
        if layout_mode != LayoutMode.SINGLE and not wrap_in:
            raise ValueError("wrap_in must be specified for MULTIPLE or NESTED layout modes")

        if wrap_mode == WrapMode.SAME:
            inner_wrap = outer_wrap = wrap_in
        elif wrap_mode == WrapMode.OTHER:
            inner_wrap = wrap_in
            outer_wrap = Row if wrap_in == Col else Col

        wrapped_components = components

        if layout_mode == LayoutMode.MULTIPLE:
            wrapped_components = [wrap_in(components=[comp], class_name=class_name) for comp in
                                  components]
        elif layout_mode == LayoutMode.NESTED:
            individually_wrapped = [wrap_in(components=[comp], class_name=class_name) for comp in
                                    components]
            wrapped_components = [
                inner_wrap(components=individually_wrapped, class_name=class_name)]


        super().__init__(components=wrapped_components, class_name=class_name)

    #
    # def __init__(
    #         self,
    #         components: list[AnyComponent],
    #         class_name: str = CSSEnum.PLAIN,
    #         layout_mode: LayoutMode = LayoutMode.SINGLE,
    #         wrap_in: Optional[type[Row] | type[Col]] = None
    # ):
    #     if layout_mode != LayoutMode.SINGLE and not wrap_in:
    #         raise ValueError("wrap_in must be specified for MULTIPLE or NESTED layout modes")
    #
    #     if layout_mode == LayoutMode.MULTIPLE:
    #         components = [wrap_in(components=[comp], class_name=class_name) for comp in components]
    #     elif layout_mode == LayoutMode.NESTED:
    #         components = [wrap_in(components=components, class_name=class_name)]
    #
    #     super().__init__(components=components, class_name=class_name)

    @classmethod
    def empty(cls) -> 'DivPR':
        return cls(components=[c.Text(text="---")])


class Row(DivPR):

    def __init__(
            self,
            components: list[AnyComponent],
            class_name: str = CSSEnum.ROW,
            layout_mode: LayoutMode = LayoutMode.SINGLE,
    ):
        super().__init__(
            components=components,
            class_name=f"row {class_name}",
            layout_mode=layout_mode,
            wrap_in=Row
        )

    @classmethod
    def headers(cls, header_names: list[str], class_name: str = CSSEnum.HEAD_ROW) -> 'Row':
        headers = [c.Div(components=[c.Text(text=_)], class_name=CSSEnum.HEAD_DIV) for _ in
                   header_names]
        return cls(components=headers, class_name=class_name, layout_mode=LayoutMode.SINGLE)


class Col(DivPR):

    def __init__(
            self,
            components: list[AnyComponent],
            class_name: str = CSSEnum.COL,
            layout_mode: LayoutMode = LayoutMode.SINGLE,
    ):
        super().__init__(
            components=components,
            class_name=f"col {class_name}",
            layout_mode=layout_mode,
            wrap_in=Col
        )


class Container(DivPR):
    def __init__(
            self,
            components: List[AnyComponent],
            class_name: str = CSSEnum.CONTAINER
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
            header_class=CSSEnum.HEAD,
            page_classname=CSSEnum.PAGE
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
                *((nav_bar,) if nav_bar else ()),
                DivPR.empty(),
            ],
        )


class LinkPR(c.Link):
    # @classmethod
    # def custom(
    #         cls,
    #         title: str,
    #         url: str,
    #         on_click: Optional[AnyEvent] = None,
    #         class_name=CSSEnum.LINK
    # ):
    #     if not url and not on_click:
    #         logger.error("Must provide url or on_click event")
    #
    #     on_click = on_click or GoToEvent(url=url)
    #
    #     return cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)

    @classmethod
    def back(cls) -> c.Link:
        title = "Back"
        on_click = BackEvent()
        class_name = CSSEnum.LINK
        return cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)

    @classmethod
    def model_nav(cls, model: RoutableModel) -> c.Link:
        return cls(
            components=[c.Text(text=model.__name__.title())],
            on_click=GoToEvent(url=model.rout_prefix()),
            active=f"startswith:{model.rout_prefix()}",
        )

    @classmethod
    def ui_link(cls, title, url, on_click=None, class_name=CSSEnum.LINK) -> LinkPR:
        on_click = on_click or GoToEvent(url=url)
        link = cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)
        return link


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
