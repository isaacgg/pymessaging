from abc import ABC, abstractmethod

from cqrs.domain.query.abc.query import Query
from shared.domain.singleton import SingletonABCMeta


class QueryHandler(ABC, metaclass=SingletonABCMeta):
    @abstractmethod
    def handle(self, query: Query):
        pass
