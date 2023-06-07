from abc import abstractmethod, ABC
from typing import Callable


class MessageConsumer(ABC):
    @abstractmethod
    def declare_queue(self, queue_name: str, **kwargs) -> None:
        ...

    @abstractmethod
    def bind(self, binding_key: str, **kwargs) -> None:
        ...

    @abstractmethod
    def consume_message(self, callback: Callable) -> None:
        ...
