from __future__ import annotations
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from ..async_ps import response_


class PageSoup(BeautifulSoup):
    """ Inject from_url classmethod into BeautifulSoup"""

    @classmethod
    async def from_url(cls, url: str, http_session: ClientSession) -> PageSoup:
        html = await response_(url, http_session)
        return cls(html, "html.parser")

    @classmethod
    def from_bs4(cls, bs4: BeautifulSoup) -> PageSoup:
        return cls(bs4.prettify(), "html.parser")

