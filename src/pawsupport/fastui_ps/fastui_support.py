from typing import List, Protocol, Sequence

from fastui.events import BackEvent, GoToEvent
from loguru import logger

from .css import COL_DFLT, ROW

try:
    from fastui import AnyComponent, components as c
except ImportError:
    logger.error("fastui not installed")


class RoutableModel(Protocol):
    @classmethod
    def rout_prefix(cls) -> str:
        ...


def Row(components: List[AnyComponent], class_name: str = ROW) -> c.Div:
    try:
        # return c.Div(components=components, class_name="row")
        if not components:
            return c.Div(components=[c.Text(text="---")])
        class_name = f"row {class_name}"
        return c.Div(components=components, class_name=class_name)
    except Exception as e:
        logger.error(e)


def Col(components: List[AnyComponent], class_name: str = COL_DFLT) -> c.Div:
    try:
        class_name = f"col {class_name}"
        return c.Div(components=components, class_name=class_name)
    except Exception as e:
        logger.error(e)


def empty_div(col=False, container=False) -> c.Div:
    if col:
        return empty_col()
    elif container:
        return empty_container()
    else:
        return c.Div(components=[c.Text(text="---")])


def empty_col():
    return Col(components=[c.Text(text="---")])


def empty_container():
    return Flex(components=[c.Text(text="---")])


def Flex(components: list[AnyComponent], class_name="") -> c.Div:
    logger.info("Flex")
    try:
        if not components:
            return c.Div(components=[c.Text(text="---")])
    except Exception as e:
        logger.error(e)
    try:
        # class_name = f"container border-bottom border-secondary {class_name}"
        # class_name = f"d-flex border-bottom border-secondary {class_name}"
        return c.Div(components=components, class_name=class_name)
    except Exception as ee:
        logger.error(ee)


def default_page(components: list[AnyComponent], title: str, navbar, header_class=None,
                 page_classname=None) -> list[AnyComponent]:
    try:
        return [
            c.PageTitle(text=title),
            navbar,
            c.Page(
                components=[
                    *((c.Heading(text=title, class_name=header_class),) if title else ()),
                    *components,
                ],
                class_name=page_classname,
            ),
            default_footer(),
        ]
    except Exception as e:
        logger.error(e)


def empty_page(nav_bar) -> list[AnyComponent]:
    return [
        c.PageTitle(text="empty page"),
        nav_bar,
        c.Page(
            components=[
                c.Heading(text="durfault title"),
                c.Text(text="---"),
            ],
        ),
        default_footer(),
    ]


def default_footer():
    return c.Footer(
        extra_text="extra durfault text",
        links=[
            c.Link(
                components=[c.Text(text="Github")],
                on_click=GoToEvent(url="https://github.com/pydantic/FastUI"),
            ),
        ],
    )


def back_link():
    return c.Link(components=[c.Text(text="Back")], on_click=BackEvent())


def nav_bar_(models: Sequence[RoutableModel]):
    return c.Navbar(
        links=[nav_link(_) for _ in models],
    )


def nav_link(model: RoutableModel):
    link = c.Link(
        components=[c.Text(text=model.__name__.title())],
        on_click=GoToEvent(url=model.rout_prefix()),
        active=f"startswith:{model.rout_prefix()}",
    )
    return link


def ui_link(title: str, url: str, on_click=None, class_name="") -> c.Link:
    if not url and not on_click:
        logger.error("No url or on_click")
        return c.Link(components=[c.Text(text="---")])
    on_click = on_click or GoToEvent(url=url)
    link = c.Link(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)
    return link
