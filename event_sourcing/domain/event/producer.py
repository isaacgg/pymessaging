from abc import ABC, abstractmethod

from event_sourcing.domain.event.message import Message


class Producer(ABC):
    @abstractmethod
    def publish(self, message: Message):
        return NotImplemented
