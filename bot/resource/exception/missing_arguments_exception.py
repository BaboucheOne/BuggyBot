class MissingArgumentsException(Exception):

    MESSAGE = (
        "Arguments manquants dans la commande. Cette commande nécessite %s arguments."
    )

    def __init__(self, number_of_arguments_needed: int):
        super().__init__(self.MESSAGE % number_of_arguments_needed)
