""""
FastUI support functions
"""
from __future__ import annotations

from typing import List, Protocol, Sequence

from fastui.events import BackEvent, GoToEvent
from loguru import logger

try:
    from fastui import AnyComponent, components as c
except ImportError as e:
    logger.error("fastui not installed")
    raise e

"""
FastUI support
"""

STANDARD = "text-center py-1 my-1"
COL_4 = f"col-4 {STANDARD}"
ROW = f'my-1 border border-bottom border-secondary rounded shadow-sm {STANDARD}'
HEAD = f'my-1 col border {STANDARD}'


class FastUiMaker:
    ...


def Row(components: List[AnyComponent], class_name: str = ROW) -> c.Div:
    """
    Create a row of fastui components

    :param components: a list of fastui components
    :param class_name: css class names as a string
    :returns: Div with class_name='row'+class_name"""
    try:
        # return c.Div(components=components, class_name="row")
        if not components:
            return c.Div(components=[c.Text(text="---")])
        class_name = f"row {class_name}"
        return c.Div(components=components, class_name=class_name)
    except Exception as e:
        logger.error(e)


def Col(components: List[AnyComponent], class_name: str = COL_4) -> c.Div:
    """
    Create a column of fastui components

    :param components: a list of fastui components
    :param class_name: css class names as a string
    :returns: Div with class_name='col'+class_name
    """

    try:
        class_name = f"col {class_name}"
        return c.Div(components=components, class_name=class_name)
    except Exception as e:
        logger.error(e)


def empty_div(col=False, container=False) -> c.Div:
    """
    Create an empty div

    :param col: if True, create an empty col
    :param container: if True, create an empty container
    :returns: Div with text '---'
    """
    if col:
        return empty_col()
    elif container:
        return empty_container()
    else:
        return c.Div(components=[c.Text(text="---")])


def empty_col():
    """
    Create an empty col

    :returns: Div with text '---' and class_name='col'
    """
    return Col(components=[c.Text(text="---")])


def empty_container():
    """
    Create an empty container

    :returns: Div with text '---' and class_name='container'
    """
    return Flex(components=[c.Text(text="---")])


def Flex(components: list[AnyComponent], class_name="") -> c.Div:
    """
    Create a flex container

    :param components: a list of fastui components
    :param class_name: css class names as a string
    :returns: Div with class_name='d-flex'+class_name
    """

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
    """
    Create a default page

    :param components: a list of fastui components
    :param title: page title
    :param navbar: navbar
    :param header_class: css class names for header as a string
    :param page_classname: css class names for page as a string
    :returns: list of fastui components
    """
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


def empty_page(nav_bar=None) -> list[AnyComponent]:
    """
    Create an empty page

    :param nav_bar: navbar
    :returns: list of fastui components
    """
    return [
        c.PageTitle(text="empty page"),
        (nav_bar if nav_bar else empty_div()),
        c.Page(
            components=[
                c.Heading(text="durfault title"),
                c.Text(text="---"),
            ],
        ),
        default_footer(),
    ]


def default_footer() -> c.Footer:
    """
    Create a default footer

    :returns: Footer with extra_text='extra durfault text' and a link to github
    """
    return c.Footer(
        extra_text="extra durfault text",
        links=[
            c.Link(
                components=[c.Text(text="Github")],
                on_click=GoToEvent(url="https://github.com/pydantic/FastUI"),
            ),
        ],
    )


def back_link() -> c.Link:
    """
    Create a back link

    :returns: Link with text='Back' and on_click=BackEvent()
    """
    return c.Link(components=[c.Text(text="Back")], on_click=BackEvent())


def nav_bar_(models: Sequence[RoutableModel]) -> c.Navbar:
    """
    Create a navbar

    :param models: a list of RoutableModel
    :returns: Navbar with links to each RoutableModel
    """
    return c.Navbar(
        links=[nav_link(_) for _ in models],
    )


def nav_link(model: RoutableModel) -> c.Link:
    """
    Create a navbar link

    :param model: a RoutableModel
    :returns: Link with text=model.__name__.title() and on_click=GoToEvent(url=model.rout_prefix())
    """
    link = c.Link(
        components=[c.Text(text=model.__name__.title())],
        on_click=GoToEvent(url=model.rout_prefix()),
        active=f"startswith:{model.rout_prefix()}",
    )
    return link


def ui_link(title: str, url: str, on_click=None, class_name="") -> c.Link:
    """
    Create a link

    :param title: link title
    :param url: link url
    :param on_click: on_click event
    :param class_name: css class names as a string
    :returns: Link with text=title and on_click=GoToEvent(url=url)
    """
    if not url and not on_click:
        logger.error("No url or on_click")
        return c.Link(components=[c.Text(text="---")])
    on_click = on_click or GoToEvent(url=url)
    link = c.Link(components=[c.Text(text=title)], on_click=on_click, class_name=class_name)
    return link


class RoutableModel(Protocol):
    """
    RoutableModel has ``rout_prefix`` classmethod
    """

    @classmethod
    def rout_prefix(cls) -> str:
        ...
