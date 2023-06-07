from abc import abstractmethod, ABC

from event_sourcing.domain.event.message import Message


class MessagePublisher(ABC):
    @property
    @abstractmethod
    def exchange(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def is_publishable(self, message: Message) -> bool:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def publish(self, messages: Message):
        raise NotImplementedError("Method not implemented")
