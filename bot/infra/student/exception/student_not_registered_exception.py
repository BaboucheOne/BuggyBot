class StudentNotRegisteredException(Exception):

    MESSAGE = "Student cannot be registered."

    def __init__(self):
        super().__init__(self.MESSAGE)
