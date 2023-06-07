from typing import Callable

from pika.connection import Connection

from event_sourcing.domain.event.message_consumer import MessageConsumer


class RabbitMqPikaConsumer(MessageConsumer):
    def __init__(self, connection: Connection, exchange: str):
        self.connection = connection
        self.channel = self.connection.channel()
        self.exchange = exchange
        self.queue_name = None

    def declare_queue(self, queue_name: str, **kwargs) -> None:
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def bind(self, binding_key: str, **kwargs) -> None:
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=kwargs["routing_key"])

    def consume_message(self, callback: Callable) -> None:
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
