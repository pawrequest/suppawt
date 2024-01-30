from __future__ import annotations

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from ..async_ps import response_


class TagSoup(BeautifulSoup):
    """Inject from_bs4 classmethod into BeautifulSoup"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_bs4(cls, bs4: BeautifulSoup) -> TagSoup:
        return cls(bs4.prettify(), "html.parser")


class PageSoup(TagSoup):
    """Inject from_url classmethod into BeautifulSoup"""

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> PageSoup:
        html = await response_(url, http_session)
        return cls(url, html, "html.parser")
