from typing import Type, Dict
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
        self.commands: Dict[Type[Command], CommandHandler] = {}
        for i in range(10):
            self.commands.update({type(f"Command{i}", (Command,), {}):
                                  MagicMock(spec=type(f"CommandHandler{i}",
                                                      (CommandHandler,), {}),
                                            instance=True)})

    def test_init(self):
        instance = SyncCommandBus(self.commands)

        for c1, c2 in zip(self.commands, instance.handlers.keys()):

            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.commands[c1].__class__, instance.handlers[c2].__class__)
        self.assertEqual(len(instance.handlers), len(self.commands))

    def test_add_commands(self):
        instance = SyncCommandBus()

        for command, command_handler in self.commands.items():
            instance.add_handler(command, command_handler)

        for c1, c2 in zip(self.commands, instance.handlers):
            self.assertEqual(c1.__class__, c2.__class__)
            self.assertEqual(self.commands[c1].__class__, instance.handlers[c2].__class__)
        self.assertEqual(len(instance.handlers), len(self.commands))

        for command, command_handler in self.commands.items():
            self.assertRaises(CommandAlreadyExistsError, instance.add_handler, command, command_handler)

    def test_dispatch_commands(self):
        instance = SyncCommandBus(self.commands)

        for command in list(self.commands.keys()):
            expected_handler = self.commands[command]
            instance.dispatch(command())

            expected_handler.execute.assert_called_once_with(InstanceOf(command))
        self.assertEqual(len(instance.handlers), len(self.commands))

    def test_command_does_not_exist(self):
        instance = SyncCommandBus(self.commands)

        self.assertEqual(len(instance.handlers), len(self.commands))
        self.assertRaises(CommandDoesNotExistError,
                          instance.dispatch,
                          type("UnknownCommand", (Command,), {}))
