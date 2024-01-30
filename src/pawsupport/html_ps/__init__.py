from .soup_selectors import AnySelectorABC, PageSelectorABC, TagSelectorABC
from .page_soup import PageSoup, TagSoup

html_entities = {
    "&": "&amp;",
    "\"": "&quot;",
    "'": "&apos;",
    "<": "&lt;",
    ">": "&gt;",
    " ": "&#32;"
}


def unsanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(entity, char)
    return string


def sanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    return string
