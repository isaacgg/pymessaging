import pika


class SyncPikaConnection:
    def __init__(self, host: str, port: int, vhost: str, username: str, password: str, heartbeat: int):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password
        self.heartbeat = heartbeat

    def connect(self) -> pika.BlockingConnection:
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials, heartbeat=self.heartbeat)
        return pika.BlockingConnection(parameters)
