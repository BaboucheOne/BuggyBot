class StudentAlreadyRegisteredException(Exception):

    MESSAGE = "Student already registered."

    def __init__(self):
        super().__init__(self.MESSAGE)
