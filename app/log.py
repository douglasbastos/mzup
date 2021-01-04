import logging


def get_logger():
    format = '{"%(levelname)s":"%(asctime)s", "%(threadName)s":"%(message)s"}'
    logging.basicConfig(format=format)
    logger = logging.getLogger('MzUp')
    logger.setLevel(logging.DEBUG)
    return logger


logger = get_logger()
