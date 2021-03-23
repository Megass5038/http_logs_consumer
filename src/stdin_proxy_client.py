import asyncio
import fileinput
from config import Config
from loguru import logger


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(Config.SERVER_HOST, Config.SERVER_PORT)
    logger.info("Connected to server")
    logger.info("Redirecting stdin to server")
    for line in fileinput.input():
        writer.write(line.encode())
        await writer.drain()
        logger.debug("Send: {}", line)


if __name__ == "__main__":
    asyncio.run(tcp_echo_client())
