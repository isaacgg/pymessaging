from unittest import TestCase
from unittest.mock import MagicMock

from callee import InstanceOf
from cqrs.domain.command.abc.command import Command
from cqrs.domain.command.abc.command_handler import CommandHandler
from cqrs.domain.command.exceptions.command_already_exists_error import CommandAlreadyExistsError
from cqrs.domain.command.exceptions.command_does_not_exist_error import CommandDoesNotExistError
from cqrs.infrastructure.messaging.command.sync_command_bus import SyncCommandBus


class TestSyncCommandBus(TestCase):
    def setUp(self):
        self.commands = {}
        for i in range(10):
            self.commands.update({type(f"Command{i}", (Command,), {}):
                                  MagicMock(spec=type(f"CommandHandler{i}",
                                                      (CommandHandler,), {}),
                                            instance=True)})

    def tearDown(self):
        for c in list(self.instance.handlers.keys()):
            self.instance.remove_handler(c)

        self.instance.handlers = {}  # This doesn't work :'(
        self.instance.__class__._instances = {}
        del self.instance

        for c in self.commands.values():
            c.reset_mock()

    def test_init(self):
        self.instance = SyncCommandBus(self.commands)

        for c1, c2 in zip(self.commands, self.instance.handlers.keys()):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.commands[c1].__class__, self.instance.handlers[c2].__class__)

    def test_add_commands(self):
        self.instance = SyncCommandBus()

        for command, command_handler in self.commands.items():
            self.instance.add_handler(command, command_handler)

        for c1, c2 in zip(self.commands, self.instance.handlers):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.commands[c1].__class__, self.instance.handlers[c2].__class__)

        for command, command_handler in self.commands.items():
            self.assertRaises(CommandAlreadyExistsError, self.instance.add_handler, command, command_handler)

    def test_dispatch_commands(self):
        self.instance = SyncCommandBus(self.commands)

        for command in list(self.commands.keys()):
            expected_handler = self.commands[command]
            self.instance.dispatch(command())
            expected_handler.execute.assert_called_once_with(InstanceOf(command))

    def test_command_does_not_exist(self):
        self.instance = SyncCommandBus(self.commands)

        self.assertRaises(CommandDoesNotExistError,
                          self.instance.dispatch,
                          type("UnknownCommand", (Command,), {}))
