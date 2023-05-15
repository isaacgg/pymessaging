from unittest import TestCase

from cqrs.domain.query.abc.query_handler import QueryHandler


class TestCommandHandler(TestCase):
    def test_singleton(self):
        qh1 = type("QH1", (QueryHandler, ), {"handle": lambda x: x})
        qh2 = type("QH2", (QueryHandler, ), {"handle": lambda x: x})

        self.assertEqual(id(qh1()), id(qh1()))
        self.assertNotEqual(id(qh1()), id(qh2()))
