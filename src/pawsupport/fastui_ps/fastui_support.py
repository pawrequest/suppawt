"""
FastUI support functions
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, Optional, Protocol, TYPE_CHECKING

from pydantic import BaseModel
from fastui.events import BackEvent, GoToEvent
from fastui import AnyComponent, components as c
from loguru import logger

if TYPE_CHECKING:
    from pawsupport.fastui_ps.types import WrapIn
_DFLT_CSS_STR = "text-center py-1 my-1"


class STYLES:
    LINK = "btn btn-primary"
    COL = "col gap-3 border"
    ROW = 'row gap-3 border'
    HEAD = ''
    CONTAINER = 'container border'
    PAGE = ''

    # HEAD_DIV = f"{PLAIN}"
    HEAD_ROW = "col border"
    TITLE_COL = "col"
    SUB_LIST = ""


def get_style(cls, css_class_name):
    inner_style = f'{getattr(STYLES, cls.__name__.upper(), '')} {css_class_name}'
    return inner_style


def all_text(*objs: BaseModel, with_keys: Literal['NO', 'YES', 'ONLY'] = 'NO') -> 'list[c.Text]':
    txts = []
    for obj in objs:
        for k, v in obj.model_dump().items():
            if not v:
                continue
            if isinstance(v, str):
                txt_str = ''
                if with_keys == 'NO':
                    txt_str = v
                elif with_keys == 'YES':
                    txt_str = f'{k} - {v}'
                elif with_keys == 'ONLY':
                    txt_str = k
                txts.append(c.Text(text=txt_str))
    return txts


# def check_wrap_mode(wparam: WrapParam):
#     if wparam.wrap_mode is not WrapMode.SINGLE, WrapMode.MULTIPLE,
#                             WrapMode.NESTED] and not wparam.wrap_inner:
#         raise ValueError()
#     if wparam.wrap_mode == WrapMode.NESTED and not wparam.wrap_outer:
#         raise ValueError()


class WrapMode(Enum):
    SINGLE = auto()  # All components in a single row/col
    # MULTIPLE = auto()  # Each component in its own row/col
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
            inner_class_name: str = '',
            outer_class_name: str = '',
            wrap_inner: Optional[WrapIn] = None,
    ) -> AnyComponent | list[AnyComponent]:

        outer_style = get_style(cls, outer_class_name)
        inner_style = get_style(wrap_inner, inner_class_name) if wrap_inner else ''

        if wrap_inner:
            components = wrap_inner.list_of(
                *components,
                class_name=inner_style,
            )

        components2 = list(components)
        ret = cls(components=components2, class_name=outer_style)
        return ret

        #     return cls.wrap(
        #         *inner_comps,
        #         inner_class_name=outer_style,
        #         wrap_mode=WrapMode.SINGLE,
        #         wrap_inner=cls
        #     )
        # else:
        #     raise ValueError(f"Invalid wrap_mode: {wrap_mode}")


    @classmethod
    # def wrap1(
    #         cls,
    #         *components: AnyComponent,
    #         inner_class_name: str = '',
    #         outer_class_name: str = '',
    #         wrap_mode: WrapMode = WrapMode.SINGLE,
    #         wrap_outer: Optional[WrapIn] = None,
    #         wrap_inner: Optional[WrapIn] = None,
    # ) -> AnyComponent | list[AnyComponent]:
    #     wrap_inner = wrap_inner or cls
    #     inner_style = get_style(wrap_inner, inner_class_name)
    #     outer_style = get_style(wrap_outer, outer_class_name) if wrap_outer else ''
    #     wparam = WrapParam(wrap_mode, wrap_inner, wrap_outer)
    #     check_wrap_mode(wparam)
    #
    #     # components are wrapped together
    #     if wrap_mode == WrapMode.SINGLE:
    #         components2 = list(components)
    #         ret = cls(components=components2, class_name=inner_style)
    #         return ret
    #
    #     # each component is wrapped in its own row or col, nested together in another row or col
    #     elif wrap_mode == WrapMode.NESTED:
    #         inner_comps = wrap_inner.list_of(
    #             *components,
    #             class_name=inner_style,
    #         )
    #         wrapped = wrap_outer.wrap(
    #             *inner_comps,
    #             inner_class_name=outer_style,
    #             wrap_mode=WrapMode.SINGLE,
    #             wrap_inner=wrap_outer
    #         )
    #     else:
    #         raise ValueError(f"Invalid wrap_mode: {wrap_mode}")
    #
    #     ret = cls.wrap(
    #         wrapped,
    #         inner_class_name=inner_class_name,
    #         wrap_mode=WrapMode.SINGLE,
    #         wrap_inner=Row
    #     )
    #     return ret

    @classmethod
    def list_of(
            cls,
            *components: AnyComponent,
            class_name: str = '',
    ) -> list[AnyComponent]:
        style = get_style(cls, class_name)
        divs = [cls(components=[comp], class_name=style)
                for comp in components]
        return divs

    @classmethod
    def empty(cls) -> 'DivPR':
        return cls(components=[c.Text(text="---")])


class Row(DivPR):
    class_name: str = STYLES.ROW

    @classmethod
    def headers(cls, header_names: list[str], class_name: str = STYLES.HEAD_ROW) -> 'Row':
        ls = [c.Text(text=_) for _ in header_names]
        return cls.wrap(*ls, class_name=class_name, wrap_mode=WrapMode.SINGLE)


class Col(DivPR):
    class_name: str = STYLES.COL


class Container(DivPR):
    class_name: str = STYLES.CONTAINER


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


class LinkPR(c.Link):
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
