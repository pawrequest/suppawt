from __future__ import annotations

from abc import ABC

from aiohttp import ClientSession
from bs4 import BeautifulSoup, ResultSet, Tag
from loguru import logger
from .async_ps import response_


class TagSelectorABC(ABC):
    def __init__(self, tag: Tag):
        self.tag = tag

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


class PageSelectorABC(TagSelectorABC, ABC):
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
