from abc import abstractmethod, ABC

from event_sourcing.domain.event.domain_event import DomainEvent


class ProcessManager(ABC):
    @abstractmethod
    def process(self, message: DomainEvent):
        ...
