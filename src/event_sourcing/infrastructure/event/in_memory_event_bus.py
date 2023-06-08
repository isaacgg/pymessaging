from typing import List, Union

from event_sourcing.domain.event.domain_event import DomainEvent
from event_sourcing.domain.event.event_bus import EventBus
from event_sourcing.domain.event.integration_event import IntegrationEvent
from event_sourcing.domain.event.message_publisher import MessagePublisher


class InMemoryEventBus(EventBus):
    def __init__(self, publishers: List[MessagePublisher]):
        self.publishers = publishers

    def publish(self, events: List[Union[DomainEvent, IntegrationEvent]]) -> None:
        for event in events:
            for publisher in self.publishers:
                if publisher.is_publishable(event):
                    publisher.publish(event)
