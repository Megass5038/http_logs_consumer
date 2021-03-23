import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 9999))
    SERVER_TEST_PORT = int(os.getenv("SERVER_TEST_PORT", 2222))
    SERVER_BUFFER_LIMIT_SIZE = int(os.getenv("SERVER_BUFFER_LIMIT_SIZE", 65536))
    REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")
    REDIS_HOUR_KEY_PREFIX = os.getenv("REDIS_KEY_PREFIX", "error_hour_")
    REDIS_HOUR_STATS_INTERVAL = int(os.getenv("REDIS_HOUR_STATS_INTERVAL", 60))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    # loguru format https://github.com/Delgan/loguru#easier-file-logging-with-rotation--retention--compression
    LOG_FILENAME = os.getenv("LOG_FILENAME")
    LOG_FILE_ROTATION = os.getenv("LOG_FILE_ROTATION", "500 MB")
