from abc import ABC, abstractmethod
from typing import Type, List

from event_sourcing.domain.event.message import Message


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: List[Type[Message]]):
        ...
