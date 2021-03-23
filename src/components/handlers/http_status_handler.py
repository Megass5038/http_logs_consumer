from .base_handler import BaseHandler
from components.items import HttpStatusItem
from components.redis_client import RedisClient
from config import Config


class HttpStatusHandler(BaseHandler):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._item = HttpStatusItem(**data)

    async def process_data(self):
        if self._item.is_weekday and self._item.is_server_error:
            redis_conn = await RedisClient.get_conn()
            hour_key = Config.REDIS_HOUR_KEY_PREFIX + str(self._item.time.hour)
            await redis_conn.execute("PFADD", hour_key, self._item.uniq_identifier)
