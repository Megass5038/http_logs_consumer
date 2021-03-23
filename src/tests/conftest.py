import pytest
import asyncio
from components import ServerWithStats, RedisClient
from config import Config


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def server():
    server = ServerWithStats(host="127.0.0.1", port=Config.SERVER_TEST_PORT)
    await server.setup()
    yield server


@pytest.fixture
async def client():
    reader, writer = await asyncio.open_connection("127.0.0.1", Config.SERVER_TEST_PORT)
    yield reader, writer
    writer.close()
    await writer.wait_closed()


@pytest.fixture
async def redis_client(monkeypatch):
    test_hour_key_prefix = "test_ " + Config.REDIS_HOUR_KEY_PREFIX
    monkeypatch.setattr(Config, "REDIS_HOUR_KEY_PREFIX", test_hour_key_prefix)
    redis_conn = await RedisClient.get_conn()
    for hour in range(24):
        hour_key = test_hour_key_prefix + str(hour)
        await redis_conn.execute("DEL", hour_key)
    yield redis_conn
    for hour in range(24):
        hour_key = test_hour_key_prefix + str(hour)
        await redis_conn.execute("DEL", hour_key)


@pytest.fixture
async def weekday_logs(client):
    logs = """{"time":"2019-05-06 17:24:53","ip":"10.0.186.98","status_code":202}
              {"time":"2019-05-06 17:24:54","ip":"10.0.121.67","status_code":301}
              {"time":"2019-05-06 17:25:54","ip":"10.0.121.67","status_code":500}
              {"time":"2019-05-06 17:26:55","ip":"10.0.121.67","status_code":500}
              {"time":"2019-05-07 16:59:55","ip":"10.0.121.67","status_code":502}
              {"time":"2019-05-07 17:00:56","ip":"10.0.247.5","status_code":503}
              {"time":"2019-05-11 10:24:57","ip":"10.0.182.224","status_code":502}
              {"time":"2019-05-11 10:24:58","ip":"10.0.117.193","status_code":401}
              {"time":"2019-05-12 10:24:59","ip":"10.0.52.162","status_code":500}
              {"time":"2020-01-01 17:24:53","ip":"10.0.186.98","status_code":502}
              {"time":"2020-01-01 17:24:54","ip":"10.0.121.67","status_code":301}
              {"time":"2020-01-01 17:25:54","ip":"10.0.121.67","status_code":500}"""
    writer = client[1]
    for line in logs.split("\n"):
        writer.write((line + "\n").encode())
        await writer.drain()
    yield logs
