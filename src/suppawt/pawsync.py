"""
functions to support async operations
"""
import asyncio

from aiohttp import ClientError, ClientSession
from loguru import logger


def quiet_cancel(func: callable) -> callable:
    """
    Async Decorator to catch CancelledError and log it quietly

    :param func: function to decorate
    :return: decorated function
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            logger.info(f"'{func.__name__}' Cancelled")
        except Exception as e:
            logger.error(f"'{func.__name__}' raised {e}")
            raise e

    return wrapper


# def quiet_cancel_try_log_as(func: callable) -> callable:
#     """
#     Decorator to catch CancelledError and log it quietly
#
#     :param func: function to decorate
#     :return: decorated function
#     """
#
#     async def wrapper(*args, **kwargs):
#         try:
#             return await func(*args, **kwargs)
#         except asyncio.CancelledError:
#             print(f"Func {func.__name__} Cancelled")
#         except Exception as e:
#             logger.error(f"Func {func.__name__} raised {e}")
#             raise e
#
#     return wrapper


async def response_(url: str, http_session: ClientSession) -> str:
    """
    Get response from url, retry 3 times if request fails

    :param url: url to get response from
    :param http_session: aiohttp ClientSession
    :return: response text
    """
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
