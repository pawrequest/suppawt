from pawsupport import get_logger

def test_logging():
    logger = get_logger(__name__)
    logger.info("Hello world")