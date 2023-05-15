from abc import ABC, abstractmethod

from cqrs.domain.command.abc.command import Command
from shared.domain.singleton import SingletonABCMeta


class CommandHandler(ABC, metaclass=SingletonABCMeta):
    @abstractmethod
    def execute(self, command: Command):
        pass
