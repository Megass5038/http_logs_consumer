from abc import ABC


class BaseHandler(ABC):
    def __init__(self, data, *args, **kwargs):
        self.data = data

    async def process_data(self):
        raise NotImplementedError
