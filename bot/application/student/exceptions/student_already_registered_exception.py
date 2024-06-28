class StudentAlreadyRegisteredException(Exception):

    MESSAGE = "The student is already registered."

    def __init__(self):
        super().__init__(self.MESSAGE)
