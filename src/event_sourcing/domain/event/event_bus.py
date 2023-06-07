from abc import ABC, abstractmethod
from typing import List, Union

from event_sourcing.domain.event.domain_event import DomainEvent
from event_sourcing.domain.event.integration_event import IntegrationEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: List[Union[DomainEvent, IntegrationEvent]]) -> None:
        raise NotImplementedError("Method not implemented")
