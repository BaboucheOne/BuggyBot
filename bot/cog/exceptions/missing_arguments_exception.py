class MissingArgumentsException(Exception):

    MESSAGE = "Missing arguments in the command. This commands required %s arguments"

    def __init__(self, number_of_arguments_needed: int):
        super().__init__(self.MESSAGE % number_of_arguments_needed)
