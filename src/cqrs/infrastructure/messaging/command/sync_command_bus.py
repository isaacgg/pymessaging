from typing import Optional, Dict, Type

from cqrs.domain.command.abc.command import Command
from cqrs.domain.command.abc.command_bus import CommandBus
from cqrs.domain.command.abc.command_handler import CommandHandler
from cqrs.domain.command.exceptions.command_already_exists_error import CommandAlreadyExistsError
from cqrs.domain.command.exceptions.command_does_not_exist_error import CommandDoesNotExistError


class SyncCommandBus(CommandBus):
    @property
    def handlers(self):
        return self._handlers

    def __init__(self, commands_map: Optional[Dict[Type[Command], CommandHandler]] = None):
        self._handlers = {}
        if commands_map is not None:
            for command, command_handler in commands_map.items():
                self.add_handler(command=command, command_handler=command_handler)

    def add_handler(self, command: Type[Command], command_handler: CommandHandler):
        if command in self.handlers:
            raise CommandAlreadyExistsError(command.__class__.__name__)
        self.handlers[command] = command_handler

    def remove_handler(self, command: Type[Command]):
        if command not in self.handlers.keys():
            raise CommandDoesNotExistError(command.__class__.__name__)
        self.handlers.pop(command)

    def dispatch(self, command: Command):
        if command.__class__ not in self.handlers:
            raise CommandDoesNotExistError(command.__class__.__name__)
        self.handlers[command.__class__].execute(command)
