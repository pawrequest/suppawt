from loguru import logger

try:
    from . import fastui_support
except ImportError as e:
    logger.warning("fastui_support not installed")
    raise e
