import pytest
import aioredis

from components import ServerWithStats
from asyncio import StreamReader, StreamWriter
from typing import Tuple
from config import Config


@pytest.mark.asyncio
async def test_server_setup(server: ServerWithStats, client: Tuple[StreamReader, StreamWriter]):
    pass


@pytest.mark.asyncio
async def test_errors_calculating(
    redis_client: aioredis.RedisConnection, server: ServerWithStats, weekday_logs: str
):
    for hour in range(24):
        hour_key = Config.REDIS_HOUR_KEY_PREFIX + str(hour)
        incidents_by_hour = await redis_client.execute("PFCOUNT", hour_key)
        if hour == 16:
            assert incidents_by_hour == 1
        elif hour == 17:
            assert incidents_by_hour == 4
        else:
            assert not incidents_by_hour
