import asyncio

import pika


class ASyncPikaConnection:
    def __init__(self, host: str, port: int, vhost: str, username: str, password: str, heartbeat: int):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password
        self.heartbeat = heartbeat

    async def connect(self) -> pika.SelectConnection:
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials, heartbeat=self.heartbeat)

        connection = await self._create_connection(parameters)
        return connection

    async def _create_connection(self, parameters: pika.ConnectionParameters) -> pika.SelectConnection:
        loop = asyncio.get_event_loop()
        connection_future = loop.create_future()

        def on_open(connection: pika.SelectConnection):
            connection_future.set_result(connection)

        connection = pika.SelectConnection(parameters, on_open_callback=on_open)
        connection.ioloop.start()

        await connection_future

        return connection
