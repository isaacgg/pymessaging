from unittest import TestCase

from cqrs.domain.command.abc.command_handler import CommandHandler


class TestCommandHandler(TestCase):
    def test_singleton(self):
        ch1 = type("CH1", (CommandHandler, ), {"execute": lambda x: x})
        ch2 = type("CH2", (CommandHandler, ), {"execute": lambda x: x})

        self.assertEqual(id(ch1()), id(ch1()))
        self.assertNotEqual(id(ch1()), id(ch2()))
