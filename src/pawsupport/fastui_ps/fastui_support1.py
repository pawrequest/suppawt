"""
FastUI support functions
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Protocol, TYPE_CHECKING

from pydantic import BaseModel
from fastui.events import BackEvent, GoToEvent
from fastui import AnyComponent, components as c
from loguru import logger

if TYPE_CHECKING:
    from pawsupport.fastui_ps.types import WrapIn
_DFLT_CSS_STR = "text-center py-1 my-1"


class STYLES:
    LINK = "btn btn-primary"
    COL = "gap10 col flexbox border border-secondary rounded shadow-sm"
    ROW = 'gap10 border border-bottom border-secondary rounded shadow-sm'
    HEAD = 'gap2 col border, flexbox'
    CONTAINER = 'flex-container gap-10 border border-secondary rounded shadow-sm'
    PAGE = ''

    # HEAD_DIV = f"{PLAIN}"
    HEAD_ROW = "my-1 col border"
    TITLE_COL = "col-4"
    SUB_LIST = ""


def check_wrap_mode(wparam: WrapParam):
    if wparam.wrap_mode in [WrapMode.SINGLE, WrapMode.MULTIPLE,
                            WrapMode.NESTED] and not wparam.wrap_inner:
        single_err = "wrap_inner must be specified for SINGLE, MULTIPLE or NESTED layout modes"
        logger.error(f"ValueError({single_err})")
        raise ValueError(single_err)
    if wparam.wrap_mode == WrapMode.NESTED and not wparam.wrap_outer:
        multiple_err = "wrap_outer must be specified for NESTED layout mode"
        logger.error(f"ValueError({multiple_err})")
        raise ValueError(multiple_err)


class WrapMode(Enum):
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
            inner_class_name: str = '',
            outer_class_name: str = '',
            wrap_inner: Optional[WrapIn],
            wrap_mode: WrapMode = WrapMode.SINGLE,
            wrap_outer: Optional[WrapIn] = None
    ) -> AnyComponent | list[AnyComponent]:

        inner_style = cls.get_inner_style(inner_class_name, wrap_inner)
        outer_style = cls.get_outer_style(outer_class_name, wrap_outer)
        wparam = WrapParam(wrap_mode, wrap_inner, wrap_outer)
        check_wrap_mode(wparam)

        # components are wrapped together
        if wrap_mode == WrapMode.SINGLE:
            components2 = list(components)
            ret = cls(components=components2, class_name=inner_style)
            return ret


        # each component is wrapped in its own row or col
        elif wrap_mode == WrapMode.MULTIPLE:
            wraps = []
            for comp in components:
                wraps.append(wrap_inner.wrap(
                    comp,
                    wrap_mode=WrapMode.SINGLE,
                    inner_class_name=inner_style,
                    wrap_inner=wrap_inner
                ))
            return wraps

        # each component is wrapped in its own row or col, nested together in another row or col
        elif wrap_mode == WrapMode.NESTED:
            inner_comps = wrap_inner.wrap(
                *components,
                inner_class_name=inner_style,
                wrap_mode=WrapMode.MULTIPLE,
                wrap_inner=wrap_inner,
            )

            wrapped = wrap_outer.wrap(
                *inner_comps,
                inner_class_name=outer_style,
                wrap_mode=WrapMode.SINGLE,
                wrap_inner=wrap_outer
            )
        else:
            raise ValueError(f"Invalid wrap_mode: {wrap_mode}")

        ret = cls.wrap(wrapped, inner_class_name=inner_class_name, wrap_mode=WrapMode.SINGLE, wrap_inner=Row)
        return ret

    @classmethod
    def get_outer_style(cls, outer_class_name, wrap_outer):
        outer_style = f'{getattr(STYLES, wrap_outer.__name__.upper())} {outer_class_name}' if wrap_outer else outer_class_name
        return outer_style

    @classmethod
    def get_inner_style(cls, inner_class_name, wrap_inner):
        inner_style = f'{getattr(STYLES, wrap_inner.__name__.upper())} {inner_class_name}' if wrap_inner else inner_class_name
        return inner_style

    @classmethod
    def empty(cls) -> 'DivPR':
        return cls(components=[c.Text(text="---")])

    @classmethod
    def all_text(
            cls,
            *objs: BaseModel,
    ) -> 'DivPR':
        txts = []
        for obj in objs:
            if not obj:
                continue
            for k, v in obj.model_dump().items():
                if not v:
                    continue
                if isinstance(v, str):
                    txts.append(c.Text(text=f'{v}'))
        return cls.wrap(
            *txts,
            wrap_mode=WrapMode.SINGLE,
            wrap_inner=Col,
        )

    @classmethod
    def all_text_with_keys(
            cls,
            *objs: BaseModel,
    ) -> 'DivPR':
        txts = []
        for obj in objs:
            if not obj:
                continue
            for k, v in obj.model_dump().items():
                if not v:
                    continue
                if isinstance(v, str):
                    txts.append(c.Text(text=f'{k} - {v}'))
        return cls.wrap(*txts, wrap_mode=WrapMode.MULTIPLE, wrap_inner=Row)


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
