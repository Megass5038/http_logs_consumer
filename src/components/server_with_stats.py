import asyncio
import json
from loguru import logger
from components.base import Server
from .redis_client import RedisClient
from config import Config


class ServerWithStats(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stats_interval = Config.REDIS_HOUR_STATS_INTERVAL
        self.__output_errors_task = None

    def create_tasks(self):
        self.__output_errors_task = self._loop.create_task(self.output_errors_by_hour())

    async def output_errors_by_hour(self):
        while True:
            conn = await RedisClient.get_conn()
            stats_by_hour = {}
            for hour in range(24):
                hour_key = Config.REDIS_HOUR_KEY_PREFIX + str(hour)
                try:
                    incidents_count = int(await conn.execute("PFCOUNT", hour_key))
                except (TypeError, ValueError):
                    incidents_count = 0
                stats_by_hour[hour] = incidents_count
            self.log_stats(stats_by_hour)
            await asyncio.sleep(self.__stats_interval)

    def log_stats(self, stats: dict):
        hour_with_max_incidents = max(stats, key=stats.get)
        if stats[hour_with_max_incidents] == 0:
            logger.info("No server errors right now")
            return
        logger.info("Current hour with maximum number of errors {}", hour_with_max_incidents)
        stats_with_errors = {k: v for k, v in stats.items() if v > 0}
        logger.info(json.dumps(stats_with_errors, indent=4))
