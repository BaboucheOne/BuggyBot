class NameTooLongException(Exception):

    MESSAGE = "Name too long."

    def __init__(self):
        super().__init__(self.MESSAGE)