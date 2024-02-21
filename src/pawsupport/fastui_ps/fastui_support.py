"""
FastUI support functions
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Protocol, TYPE_CHECKING

from fastui.events import BackEvent, GoToEvent
from fastui import AnyComponent, components as c

if TYPE_CHECKING:
    from pawsupport.fastui_ps.types import WrapIn
_DFLT_CSS_STR = "text-center py-1 my-1"


class STYLES:
    LINK = "btn btn-primary"
    COL = "col"
    ROW = 'my-1 border border-bottom border-secondary rounded shadow-sm'
    HEAD = 'my-1 col border'
    CONTAINER = 'container'
    PAGE = ''

    # HEAD_DIV = f"{PLAIN}"
    HEAD_ROW = "my-1 col border"
    TITLE_COL = "col-4"
    SUB_LIST = ""


def check_wrap_mode(wparam: WrapParam):
    if wparam.wrap_mode not in ([WrapMode.SINGLE, WrapMode.NONE]):
        if not wparam.wrap_inner:
            raise ValueError("wrap_in must be specified for MULTIPLE or NESTED layout modes")
        if wparam.wrap_mode == WrapMode.NESTED and not wparam.wrap_outer:
            raise ValueError(
                "wrap_inner and wrap_outer must be specified for NESTED layout mode"
            )


class WrapMode(Enum):
    NONE = auto()  # No wrapping
    SINGLE = auto()  # All components in a single row/col
    MULTIPLE = auto()  # Each component in its own row/col
    NESTED = auto()  # Each component in its own row/col, all nested in another row/col


@dataclass
class WrapParam:
    wrap_mode: WrapMode
    wrap_inner: Optional[WrapIn]
    wrap_outer: Optional[WrapIn]


class DivPR(c.Div):
    @classmethod
    def wrap(
            cls,
            *components: AnyComponent,
            class_name: str = '',
            wrap_mode: WrapMode = WrapMode.NONE,
            wrap_inner: Optional[WrapIn] = None,
            wrap_outer: Optional[WrapIn] = None
    ):
        wparam = WrapParam(wrap_mode, wrap_inner, wrap_outer)
        check_wrap_mode(wparam)

        # components are not wrapped
        if wrap_mode == WrapMode.NONE:
            components2 = list(components)
            ret = cls(components=components2, class_name=class_name)
            return ret

        # components are wrapped together in a single row or col
        elif wrap_mode == WrapMode.SINGLE:
            wrapped = wrap_inner.wrap(*components, class_name=class_name, wrap_mode=WrapMode.NONE)

        # each component is wrapped in its own row or col
        elif wrap_mode == WrapMode.MULTIPLE:
            wrappees = [wrap_inner.wrap(_, class_name=class_name, wrap_mode=WrapMode.NONE) for _ in
                        components]
            # wrapped = wrap_inner.wrap(*wrappees, class_name=class_name, wrap_mode=WrapMode.SINGLE)
            return wrappees


        # each component is wrapped in its own row or col, nested together in another row or col
        elif wrap_mode == WrapMode.NESTED:
            wrapped_inner = wrap_inner.wrap(
                *components,
                class_name=class_name,
                wrap_mode=WrapMode.MULTIPLE,
                wrap_inner=wrap_inner
            )

            wrapped = wrap_outer.wrap(
                *wrapped_inner,
                class_name=class_name,
                wrap_mode=WrapMode.NONE
            )
        else:
            raise ValueError(f"Invalid wrap_mode: {wrap_mode}")

        return cls.wrap(wrapped, class_name=class_name, wrap_mode=WrapMode.NONE)

    # @model_validator(mode='after')
    # def check_wrap_mode(self):
    #     if self.wrap_mode not in ([WrapMode.SINGLE, WrapMode.NONE]):
    #         if not self.wrap_inner:
    #             raise ValueError("wrap_in must be specified for MULTIPLE or NESTED layout modes")
    #         if self.wrap_mode and self.wrap_mode == WrapMode.NESTED and not self.wrap_outer:
    #             raise ValueError(
    #                 "wrap_inner and wrap_outer must be specified for NESTED layout mode"
    #             )

    @classmethod
    def empty(cls) -> 'DivPR':
        return cls(components=[c.Text(text="---")])


class Row(DivPR):
    class_name: str = "row"

    @classmethod
    def wrap(
            cls,
            *components: AnyComponent,
            class_name: str = '',
            wrap_mode: WrapMode = WrapMode.NONE,
            wrap_inner: Optional[WrapIn] = None,
            wrap_outer: Optional[WrapIn] = None
    ):
        return super().wrap(
            *components,
            class_name=f'row {class_name}',
            wrap_mode=wrap_mode,
            wrap_inner=wrap_inner,
            wrap_outer=wrap_outer
        )

    # def __init__(
    #         self,
    #         *components: AnyComponent,
    #         class_name: str = CSSEnum.ROW,
    #         wrap_mode: WrapMode = WrapMode.NONE,
    # ):
    #     super().__init__(
    #         *components,
    #         class_name=f"row {class_name}",
    #         wrap_mode=wrap_mode,
    #         wrap_inner=Row
    #     )

    @classmethod
    def headers(cls, header_names: list[str], class_name: str = STYLES.HEAD_ROW) -> 'Row':
        ls = [c.Text(text=_) for _ in header_names]
        return cls.wrap(*ls, class_name=class_name, wrap_mode=WrapMode.SINGLE)

    # @classmethod
    # def headers1(cls, header_names: list[str], class_name: str = CSSEnum.HEAD_ROW) -> 'Row':
    #     headers = [c.Div(components=[c.Text(text=_)], class_name=CSSEnum.HEAD_DIV) for _ in
    #                header_names]
    #     return cls(components=headers, class_name=class_name, wrap_mode=WrapMode.SINGLE)


class Col(DivPR):
    class_name: str = "col"

    @classmethod
    def wrap(
            cls,
            *components: AnyComponent,
            class_name: str = '',
            wrap_mode: WrapMode = WrapMode.NONE,
            wrap_inner: Optional[WrapIn] = None,
            wrap_outer: Optional[WrapIn] = None
    ):
        return super().wrap(
            *components,
            class_name=f'col {class_name}',
            wrap_mode=wrap_mode,
            wrap_inner=wrap_inner,
            wrap_outer=wrap_outer
        )

    # def __init__(
    #         self,
    #         *components: AnyComponent,
    #         class_name: str = CSSEnum.COL,
    #         wrap_mode: WrapMode = WrapMode.NONE,
    #         wrap_inner: Optional[WrapIn] = None,
    #         wrap_outer: Optional[WrapIn] = None,
    # ):
    #     super().__init__(
    #         *components,
    #         class_name=f"col {class_name}",
    #         wrap_mode=wrap_mode,
    #         wrap_inner=wrap_inner,
    #         wrap_outer=wrap_outer
    #
    #     )


class Container(DivPR):
    @classmethod
    def wrap(
            cls,
            *components: AnyComponent,
            class_name: str = '',
            wrap_mode: WrapMode = WrapMode.NONE,
            wrap_inner: Optional[WrapIn] = None,
            wrap_outer: Optional[WrapIn] = None
    ):
        return super().wrap(
            *components,
            class_name=f'container {class_name}',
            wrap_mode=wrap_mode,
            wrap_inner=wrap_inner,
            wrap_outer=wrap_outer
        )


@classmethod
def from_list(cls, *components: AnyComponent, class_name: str = '') -> DivPR:
    return cls(*components, class_name=class_name)


@classmethod
def empty(cls):
    return cls(DivPR.empty())


class PagePR(c.Page):
    @classmethod
    def default_page(
            cls,
            *components: AnyComponent,
            title: str = '',
            navbar=None,
            footer=None,
            header_class=STYLES.HEAD,
            class_name=STYLES.PAGE
    ) -> list[AnyComponent]:
        return [
            c.PageTitle(text=f'PawRequest dev - {title}' if title else ''),
            *((navbar,) if navbar else ()),
            c.Page(
                components=[
                    *((c.Heading(text=title, class_name=header_class),) if title else ()),
                    *components,
                ],
                class_name=class_name,
            ),
            *((footer,) if footer else ()),
        ]

    @classmethod
    def empty_page(cls, nav_bar=None) -> list[AnyComponent]:
        return cls.default_page(
            c.Heading(text="empty page"),
            *((nav_bar,) if nav_bar else ()),
            DivPR.empty(),
            title="empty page",
        )


#
# class PagePR1(c.Page):
#     @classmethod
#     def default_page(
#             cls,
#             components: list[AnyComponent],
#             title: str = '',
#             navbar=None,
#             footer=None,
#             header_class=CSSEnum.HEAD,
#             page_classname=CSSEnum.PAGE
#     ) -> list[AnyComponent]:
#         return [
#             c.PageTitle(text=f'PawRequest dev - {title}' if title else ''),
#             *((navbar,) if navbar else ()),
#             c.Page(
#                 components=[
#                     *((c.Heading(text=title, class_name=header_class),) if title else ()),
#                     *components,
#                 ],
#                 class_name=page_classname,
#             ),
#             *((footer,) if footer else ()),
#         ]
#
#     @classmethod
#     def empty_page(cls, nav_bar=None) -> list[AnyComponent]:
#         return cls.default_page(
#             title="empty page",
#             components=[
#                 c.Heading(text="empty page"),
#                 *((nav_bar,) if nav_bar else ()),
#                 DivPR.empty(),
#             ],
#         )


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
        class_name = STYLES.LINK
        return cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)

    @classmethod
    def model_nav(cls, model: RoutableModel) -> c.Link:
        return cls(
            components=[c.Text(text=model.__name__.title())],
            on_click=GoToEvent(url=model.rout_prefix()),
            active=f"startswith:{model.rout_prefix()}",
        )

    @classmethod
    def ui_link(cls, title, url, on_click=None, class_name=STYLES.LINK) -> LinkPR:
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
