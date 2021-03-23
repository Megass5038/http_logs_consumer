import aioredis
from config import Config


class RedisClient:
    __conn = None

    @classmethod
    async def get_conn(cls) -> aioredis.RedisConnection:
        if cls.__conn is None:
            cls.__conn = await aioredis.create_connection(Config.REDIS_ADDRESS)
        return cls.__conn
