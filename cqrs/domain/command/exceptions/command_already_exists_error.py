class CommandAlreadyExistsError(Exception):
    def __init__(self, command_name):
        self.message = f'Unable to register command. {command_name} already exist'
        super(CommandAlreadyExistsError, self).__init__()
