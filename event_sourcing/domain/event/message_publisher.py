from abc import abstractmethod, ABC

from event_sourcing.domain.event.message import Message


class MessagePublisher(ABC):
    exchange: str = NotImplemented
    aggregate: str = NotImplemented
    messages = []

    @abstractmethod
    def publish(self, message: Message):
        return NotImplemented

    @abstractmethod
    def is_publishable(self, message: Message) -> bool:
        return NotImplemented

    @abstractmethod
    def declare_exchange(self):
        return NotImplemented
