from datetime import datetime


class HttpStatusItem:
    def __init__(self, time: str, ip: str, status_code: int):
        self.__ip = ip
        self.__time = time
        self.__status_code = status_code

    @property
    def ip(self) -> str:
        return self.__ip

    @property
    def time(self) -> datetime:
        return datetime.strptime(self.__time, "%Y-%m-%d %H:%M:%S")

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def is_weekday(self) -> bool:
        return self.time.weekday() < 5

    @property
    def is_server_error(self) -> bool:
        return 500 <= self.__status_code < 600

    @property
    def uniq_identifier(self) -> str:
        return f"{self.time.strftime('%Y-%m-%d %H')}_{self.__ip}"
