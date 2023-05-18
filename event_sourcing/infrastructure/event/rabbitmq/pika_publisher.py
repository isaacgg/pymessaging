import json
from typing import List, Tuple, Union, Type

from pika.connection import Connection

from event_sourcing.domain.event.domain_event import DomainEvent
from event_sourcing.domain.event.integration_event import IntegrationEvent
from event_sourcing.domain.event.message_publisher import MessagePublisher


class PikaPublisher(MessagePublisher):
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

    def _is_processabe(self, domain_event: Union[DomainEvent, IntegrationEvent]) -> bool:
        return isinstance(domain_event, self.publishable_events)

    def publish(self, messages: List[Union[DomainEvent, IntegrationEvent]]):
        for message in messages:
            self.connection.channel() \
                .basic_publish(exchange=self.exchange,
                               routing_key=message.routing_key,
                               body=json.dumps(message.serialize()))
