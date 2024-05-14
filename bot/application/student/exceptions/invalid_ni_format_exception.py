class InvalidNIFormatException(Exception):

    MESSAGE = "The provided NI does not match the format.\nMake sure that the format is corresponding to 9 digits."

    def __init__(self):
        super().__init__(self.MESSAGE)
