class InvalidNameFormatException(RuntimeError):

    MESSAGE = "%s ne correspond pas au format."

    def __init__(self, name: str):
        super().__init__(self.MESSAGE % repr(name))
