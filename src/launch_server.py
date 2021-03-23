from components import ServerWithStats
from config import Config
from utils import configure_loguru


if __name__ == "__main__":
    configure_loguru(Config.LOG_LEVEL, Config.LOG_FILENAME, Config.LOG_FILE_ROTATION)
    server = ServerWithStats(
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        buffer_limit=Config.SERVER_BUFFER_LIMIT_SIZE,
    )
    server.launch()
