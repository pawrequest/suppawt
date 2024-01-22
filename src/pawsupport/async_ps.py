import asyncio

from aiohttp import ClientSession, ClientError
from loguru import logger


def quiet_cancel_as(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            print(f"Func {func.__name__} Cancelled")

    return wrapper


def quiet_cancel_try_log_as(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            print(f"Func {func.__name__} Cancelled")
        except Exception as e:
            logger.error(f"Func {func.__name__} raised {e}")

    return wrapper


async def response_(url: str, http_session: ClientSession):
    """Get response from url, retry 3 times if request fails"""
    for _ in range(3):
        try:
            async with http_session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except ClientError as e:
            logger.error(f"Request failed: {e}")
            await asyncio.sleep(2)
            continue
    else:
        raise ClientError("Request failed 3 times")
