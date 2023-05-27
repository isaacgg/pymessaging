from unittest import TestCase
from unittest.mock import MagicMock

from callee import InstanceOf

from cqrs.domain.query.abc.query import Query
from cqrs.domain.query.abc.query_handler import QueryHandler
from cqrs.domain.query.exceptions.query_already_exists_error import QueryAlreadyExistsError
from cqrs.domain.query.exceptions.query_does_not_exist_error import QueryDoesNotExistError
from cqrs.infrastructure.messaging.query.sync_query_bus import SyncQueryBus


class TestSyncQueryBus(TestCase):
    def setUp(self):
        self.queries = {}
        for i in range(10):
            self.queries.update({type(f"Query{i}", (Query,), {}):
                                 MagicMock(spec=type(f"QueryHandler{i}", (QueryHandler,), {}), instance=True)})

    def test_init(self):
        instance = SyncQueryBus(self.queries)

        for c1, c2 in zip(self.queries, instance.handlers.keys()):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.queries[c1].__class__, instance.handlers[c2].__class__)
        self.assertEqual(len(instance.handlers), len(self.queries))

    def test_add_queries(self):
        instance = SyncQueryBus()

        for query, query_handler in self.queries.items():
            instance.add_handler(query, query_handler)

        for c1, c2 in zip(self.queries, instance.handlers):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.queries[c1].__class__, instance.handlers[c2].__class__)
        self.assertEqual(len(instance.handlers), len(self.queries))

        for query, query_handler in self.queries.items():
            self.assertRaises(QueryAlreadyExistsError, instance.add_handler, query, query_handler)

    def test_dispatch_queries(self):
        instance = SyncQueryBus(self.queries)

        for query in list(self.queries.keys()):
            expected_handler = self.queries[query]
            instance.ask(query())

            expected_handler.handle.assert_called_once_with(InstanceOf(query))
        self.assertEqual(len(instance.handlers), len(self.queries))

    def test_query_does_not_exist(self):
        instance = SyncQueryBus(self.queries)

        self.assertEqual(len(instance.handlers), len(self.queries))
        self.assertRaises(QueryDoesNotExistError,
                          instance.ask,
                          type("UnknownQuery", (Query,), {}))
