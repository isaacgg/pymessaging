from abc import ABC, abstractmethod

from cqrs.domain.query.abc.query import Query


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query):
        pass
