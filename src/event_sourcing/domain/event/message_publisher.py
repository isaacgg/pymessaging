from abc import abstractmethod, ABC
from typing import List

from event_sourcing.domain.event.message import Message


class MessagePublisher(ABC):
    @property
    @abstractmethod
    def exchange(self):
        return

    @abstractmethod
    def publish(self, messages: List[Message]):
        return NotImplemented
