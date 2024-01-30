from __future__ import annotations

"""
Abstract base classes for selecting text and links from BeautifulSoup Tag objects.
Create a subclass for each site to be scraped with methods for selecting text and links.
"""
from abc import ABC  # noqa: E402 surely a better way to avoid pycharm warning

from aiohttp import ClientSession  # noqa: E402
from bs4 import BeautifulSoup, Tag  # noqa: E402
from loguru import logger  # noqa: E402

from ..async_ps import response_  # noqa: E402


class TagSelectorABC(ABC):
    """ Abstract base class for selecting text and links from BeautifulSoup Tag objects."""

    def __init__(self, tag: Tag, name=None):
        self.tag = tag
        self.name = name or self.__class__.__name__

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> TagSelectorABC:
        try:
            html = await response_(url, http_session)
            soup = BeautifulSoup(html, "html.parser")
            return cls(soup)
        except Exception as e:
            logger.error(f"Error getting {url}: {e}", category="Scraper")
            raise e

    def select_text(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs).text.strip()

    def select_link(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs)["href"]


class PageSelectorABC(TagSelectorABC):
    def __init__(self, tag: Tag, url):
        try:
            super().__init__(tag)
            self.url = url
        except Exception as e:
            logger.error(f"Error getting {url}: {e}", category="Scraper")

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> PageSelectorABC:
        try:
            html = await response_(url, http_session)
            soup = BeautifulSoup(html, "html.parser")
            return cls(soup, url)
        except Exception as e:
            logger.error(f"Error getting {url}: {e}", category="Scraper")


class AnySelectorABC(ABC):
    def __init__(self, tag: Tag, url: str = None):
        try:
            self.tag = tag
            self.url = url
        except Exception as e:
            logger.error(f"Error getting {url}: {e}", category="Scraper")

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> AnySelectorABC:
        try:
            html = await response_(url, http_session)
            soup = BeautifulSoup(html, "html.parser")
            return cls(soup, url)
        except Exception as e:
            logger.error(f"Error getting {url}: {e}", category="Scraper")

    def select_text(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs).text.strip()

    def select_link(self, *args, **kwargs) -> str:
        return self.tag.select_one(*args, **kwargs)["href"]
