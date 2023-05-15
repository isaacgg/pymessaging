import json

from pika.connection import Connection

from event_sourcing.domain.event.message import Message
from event_sourcing.domain.event.message_publisher import MessagePublisher


class PikaPublisher(MessagePublisher):
    def __init__(self, connection: Connection, exchange):
        self.connection = connection
        self.exchange = exchange

        self.declare_exchange()

    def declare_exchange(self) -> None:
        self.connection.channel().exchange_declare(exchange=self.exchange,
                                                   exchange_type='topic')

    def is_publishable(self, message: Message) -> bool:
        return message.aggregate == self.aggregate

    def publish(self, message: Message):
        if self.is_publishable(message=message):
            self.connection.channel() \
                .basic_publish(exchange=self.exchange,
                               routing_key=message.routing_key,
                               body=json.dumps(message.serialize()))
