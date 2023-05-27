from typing import Type, Dict, Optional

from cqrs.domain.query.abc.query import Query
from cqrs.domain.query.abc.query_bus import QueryBus
from cqrs.domain.query.abc.query_handler import QueryHandler
from cqrs.domain.query.exceptions.query_already_exists_error import QueryAlreadyExistsError
from cqrs.domain.query.exceptions.query_does_not_exist_error import QueryDoesNotExistError


class SyncQueryBus(QueryBus):
    @property
    def handlers(self):
        return self._handlers

    def __init__(self, queries_map: Optional[Dict[Type[Query], Type[QueryHandler]]] = None):
        self._handlers = {}
        if queries_map is not None:
            for query, query_handler in queries_map.items():
                self.add_handler(query=query, query_handler=query_handler)

    def add_handler(self, query: Type[Query], query_handler: Type[QueryHandler]):
        if query in self.handlers:
            raise QueryAlreadyExistsError(query.__class__.__name__)
        self.handlers[query] = query_handler

    def remove_handler(self, query: Type[Query]):
        if query not in self.handlers.keys():
            raise QueryDoesNotExistError(query.__class__.__name__)
        self.handlers.pop(query)

    def ask(self, query: Query):
        if query.__class__ not in self.handlers:
            raise QueryDoesNotExistError(query.__class__.__name__)
        return self.handlers[query.__class__].handle(query)
