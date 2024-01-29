"""
exception types
"""
from loguru import logger



def try_except_log_as(func):
    """
    Decorator to catch exceptions on async funcs and log them

    :param func: async function to decorate
    :return: decorated async function
    """
    logger.warning(f'try_except_log: is only for dev - {func.__name__}')

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            calling_func = func.__name__
            logger.error(
                f'{calling_func} raised {str(e)} with args {str(*args)} and kwargs {str(**kwargs)}')

    return wrapper
