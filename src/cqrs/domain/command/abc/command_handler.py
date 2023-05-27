from abc import ABC, abstractmethod

from cqrs.domain.command.abc.command import Command


class CommandHandler(ABC):
    @abstractmethod
    def execute(self, command: Command):
        pass
