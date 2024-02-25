"""
FastUI support functions
"""
from __future__ import annotations

from enum import Enum, auto
from typing import Literal, Optional, Protocol, TYPE_CHECKING

from pydantic import BaseModel
from fastui.events import BackEvent, GoToEvent
from fastui import AnyComponent, components as c

from pawsupport.fastui_ps import css

if TYPE_CHECKING:
    from pawsupport.fastui_ps.types import ContainerLike


class Link(c.Link):
    ...


class Text(c.Text):
    @classmethod
    def all_text(
            cls,
            *objs: BaseModel,
            with_keys: Literal['NO', 'YES', 'ONLY'] = 'NO'
    ) -> 'list[Text]':
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
                    txts.append(cls(text=txt_str))
        return txts


class WrapMode(Enum):
    SINGLE = auto()  # All components in a single row/col
    NESTED = auto()  # Each component in its own row/col, all nested in another row/col


class DivPR(c.Div):
    @classmethod
    def wrap(
            cls,
            *components: AnyComponent,
            inner_class_name: str = '',
            outer_class_name: str = '',
            wrap_inner: Optional[ContainerLike] = None,
    ) -> AnyComponent | list[AnyComponent]:
        outer_style = style_by_cls_name(cls, outer_class_name)
        inner_style = style_by_cls_name(wrap_inner, inner_class_name) if wrap_inner else ''

        if wrap_inner:
            components = wrap_inner.list_of(
                *components,
                class_name=inner_style,
            )

        components2 = list(components)
        ret = cls(components=components2, class_name=outer_style)
        return ret

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
    class_name: str = css.ROW


class Col(DivPR):
    class_name: str = css.COL


class Container(DivPR):
    class_name: str = css.CONTAINER


def get_style(cls, css_class_name):
    inner_style = f'{getattr(css, cls.__name__.upper(), '')} {css_class_name}'
    return inner_style


_DFLT_CSS_STR = "text-center py-1 my-1"


class PagePR(c.Page):
    @classmethod
    def default_page(
            cls,
            *components: AnyComponent,
            title: str = '',
            navbar=None,
            footer=None,
            header_class=css.HEAD,
            class_name=css.PAGE
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
        class_name = css.LINK
        return cls(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)

    @classmethod
    def model_nav(cls, model: RoutableModel) -> c.Link:
        return cls(
            components=[c.Text(text=model.__name__.title())],
            on_click=GoToEvent(url=model.rout_prefix()),
            active=f"startswith:{model.rout_prefix()}",
        )

    @classmethod
    def ui_link(cls, title, url, on_click=None, class_name=css.LINK) -> LinkPR:
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


def style_by_cls_name(cls, css_class_name):
    inner_style = f'{getattr(css, cls.__name__.upper(), '')} {css_class_name}'
    return inner_style
