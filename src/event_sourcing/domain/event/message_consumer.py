from abc import abstractmethod, ABC
from typing import Dict, Callable


class MessageConsumer(ABC):
    @abstractmethod
    def declare_queue(self, queue_name: str, options: Dict) -> None:
        ...

    @abstractmethod
    def bind(self, binding_key: str, options: Dict) -> None:
        ...

    @abstractmethod
    def consume_message(self, callback: Callable) -> None:
        ...
