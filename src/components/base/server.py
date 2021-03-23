import asyncio
import traceback
import json

from asyncio import events, StreamReader, StreamWriter
from asyncio.streams import StreamReaderProtocol
from loguru import logger
from typing import Optional
from components.handlers import HttpStatusHandler


class Server:
    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 9999,
        buffer_limit: int = 2 ** 16,
        messages_separator: str = "\n",
    ):
        self.host = host
        self.port = port
        self.buffer_limit = buffer_limit
        self.messages_separator = messages_separator.encode()
        self._loop = None
        self._server: Optional[asyncio.base_events.Server] = None

    async def _handle_echo(self, reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info("peername")
        try:
            while data := await reader.readuntil(separator=self.messages_separator):
                message = data.decode().strip()
                logger.debug('Received "{message}" from {addr}', message=message, addr=addr)
                await self._handle_message(message, addr)
        except asyncio.IncompleteReadError as e:
            pass
        writer.close()
        await writer.wait_closed()
        logger.debug("Connection with {addr} was closed", addr=addr)

    def _handle_exception(self, loop, context):
        msg = context.get("exception", context["message"])
        logger.error("Unhandled exception occurred: {msg}", msg=msg)

    async def _handle_message(self, message: str, addr: tuple):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            logger.error(
                'Cannot convert message "{msg}" to JSON. Skipping it ({addr})',
                msg=message,
                addr=addr,
            )
            return
        handlers = self._choose_handlers(data)
        for handler in handlers:
            try:
                handler_instance = handler(data)
                await handler_instance.process_data()
            except Exception as e:
                logger.error(
                    "Unhandled exception occurred while processing {data} with {handler} ({addr}): {error}",
                    data=data,
                    handler=handler.__name__,
                    addr=addr,
                    error=repr(e),
                )
                logger.error(traceback.format_exc())

    def _choose_handlers(self, data):
        """
        Method for selecting data handlers depending on the message
        :param data:
        :return:
        """
        return [HttpStatusHandler]

    async def _create_loop(self):
        self._loop = events.get_event_loop()
        self._loop.set_exception_handler(self._handle_exception)

    async def _create_server(self):
        def factory():
            reader = StreamReader(limit=self.buffer_limit, loop=self._loop)
            protocol = StreamReaderProtocol(reader, self._handle_echo, loop=self._loop)
            return protocol

        self._server = await self._loop.create_server(factory, self.host, self.port)

    def create_tasks(self):
        pass

    async def _serve(self):
        await self.setup()
        addr = self._server.sockets[0].getsockname()
        logger.info("Serving on {addr}", addr=addr)
        async with self._server:
            await self._server.serve_forever()

    def get_loop(self):
        return self._loop

    async def setup(self):
        await self._create_loop()
        self.create_tasks()
        await self._create_server()

    def launch(self):
        asyncio.run(self._serve())
