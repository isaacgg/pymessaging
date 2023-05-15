import pika
from pika.connection import Connection


class SyncPikaConnection:
    HEARTBEAT = 4

    def __init__(self, host: str, port: int, vhost: str, username: str, password: str):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password

    def connect(self) -> pika.BlockingConnection:
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials, heartbeat=self.HEARTBEAT)
        return pika.BlockingConnection(parameters)
