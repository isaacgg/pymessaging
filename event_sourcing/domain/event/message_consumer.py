from abc import abstractmethod, ABC


class MessageConsumer(ABC):
    @property
    @abstractmethod
    def channel(self):
        ...

    @abstractmethod
    def consume(self):
        ...
