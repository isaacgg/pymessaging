from abc import ABC, abstractmethod
from typing import Any

from cqrs.domain.query.abc.query import Query
from cqrs.domain.query.abc.query_handler import QueryHandler


class QueryBus(ABC):
    @property
    @abstractmethod
    def handlers(self):
        ...

    @abstractmethod
    def add_handler(self, query: Query, query_handler: QueryHandler) -> None:
        ...

    @abstractmethod
    def ask(self, query: Query) -> Any:
        ...
