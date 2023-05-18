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

    def tearDown(self):
        for c in list(self.instance.handlers.keys()):
            self.instance.remove_handler(c)

        self.instance.handlers = {}  # This doesn't work :'(
        self.instance.__class__._instances = {}
        del self.instance

        for c in self.queries.values():
            c.reset_mock()

    def test_init(self):
        self.instance = SyncQueryBus(self.queries)

        for c1, c2 in zip(self.queries, self.instance.handlers.keys()):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.queries[c1].__class__, self.instance.handlers[c2].__class__)

    def test_add_queries(self):
        self.instance = SyncQueryBus()

        for query, query_handler in self.queries.items():
            self.instance.add_handler(query, query_handler)

        for c1, c2 in zip(self.queries, self.instance.handlers):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.queries[c1].__class__, self.instance.handlers[c2].__class__)

        for query, query_handler in self.queries.items():
            self.assertRaises(QueryAlreadyExistsError, self.instance.add_handler, query, query_handler)

    def test_dispatch_queries(self):
        self.instance = SyncQueryBus(self.queries)

        for query in list(self.queries.keys()):
            expected_handler = self.queries[query]
            self.instance.ask(query())
            expected_handler.handle.assert_called_once_with(InstanceOf(query))

    def test_query_does_not_exist(self):
        self.instance = SyncQueryBus(self.queries)

        self.assertRaises(QueryDoesNotExistError,
                          self.instance.ask,
                          type("UnknownQuery", (Query,), {}))
