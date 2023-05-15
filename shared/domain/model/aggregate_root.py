from typing import List

from shared.domain.bus.event.domain_event import DomainEvent
from shared.domain.model.aggregate_id import AggregateId


class AggregateRoot:
    def __init__(self, id: AggregateId):
        self._version = 0
        self._id = id
        self._domain_events = []
        if self.__class__.__name__ == 'AggregateRoot':
            raise NotImplementedError("You can't instantiate this abstract class. Derive it, please.")

    def id(self) -> AggregateId:
        return self._id

    def version(self) -> int:
        return self._version

    def record(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def recorded_events(self) -> List:
        aux = self._domain_events
        self._domain_events = []
        return aux

    def __eq__(self, other) -> bool:
        if not isinstance(other, AggregateRoot):
            return False
        return other.id().id == self.id().id

    def __hash__(self) -> int:
        return hash(self.id().id)
