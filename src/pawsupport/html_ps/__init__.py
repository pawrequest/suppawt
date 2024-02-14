from loguru import logger

try:
    from .soup_selectors import AnySelectorABC, PageSelectorABC, TagSelectorABC
    from .page_soup import PageSoup, TagSoup
except ImportError:
    logger.warning("BeautifulSoup not installed")

html_entities = {
    r"&": r"&amp;",
    r'"': r"&quot;",
    r"'": r"&apos;",
    r"<": r"&lt;",
    r">": r"&gt;",
    r" ": r"&#32;"
}


def unsanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(entity, char)
    return string


def sanitise(string):
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    return string
