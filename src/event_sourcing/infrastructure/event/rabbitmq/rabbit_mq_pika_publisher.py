import json
from typing import Tuple, Union, Type

from pika.connection import Connection

from event_sourcing.domain.event.domain_event import DomainEvent
from event_sourcing.domain.event.integration_event import IntegrationEvent
from event_sourcing.domain.event.message_publisher import MessagePublisher


class RabbitMqPikaPublisher(MessagePublisher):
    exchange = None

    def __init__(self,
                 connection: Connection,
                 exchange: str,
                 publishable_events: Tuple[Union[Type[DomainEvent], Type[IntegrationEvent]], ...]):
        self.connection = connection
        self.exchange = exchange
        self.publishable_events = publishable_events

        self._declare_exchange_if_not_exist()

    def _declare_exchange_if_not_exist(self) -> None:
        self.connection.channel().exchange_declare(exchange=self.exchange,
                                                   exchange_type='topic')

    def is_publishable(self, domain_event: Union[DomainEvent, IntegrationEvent]) -> bool:
        return isinstance(domain_event, self.publishable_events)

    def publish(self, message: Union[DomainEvent, IntegrationEvent]):
        if self.is_publishable(message):
            self.connection.channel() \
                .basic_publish(exchange=self.exchange,
                               routing_key=message.get_routing_key(),
                               body=json.dumps(message.serialize()))
