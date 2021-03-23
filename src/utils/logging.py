import sys

from loguru import logger


def configure_loguru(log_level: str, log_filename=None, log_file_rotation=None):
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    if log_filename:
        logger.add(log_filename, rotation=log_file_rotation, level=log_level)
