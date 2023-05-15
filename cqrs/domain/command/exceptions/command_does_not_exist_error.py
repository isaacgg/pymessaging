class CommandDoesNotExistError(Exception):
    def __init__(self, command_name):
        self.message = f'Unable to execute command. {command_name} does not exist'
        super(CommandDoesNotExistError, self).__init__()
