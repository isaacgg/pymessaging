from abc import abstractmethod, ABC

from cqrs.domain.command.abc.command import Command
from cqrs.domain.command.abc.command_handler import CommandHandler
from shared.domain.singleton import SingletonABCMeta


class CommandBus(ABC, metaclass=SingletonABCMeta):
    @property
    @abstractmethod
    def handlers(self):
        pass

    @abstractmethod
    def add_handler(self, command: Command, command_handler: CommandHandler):
        pass

    @abstractmethod
    def dispatch(self, command: Command):
        pass
