class StudentAlreadyExistsException(Exception):

    MESSAGE = "The student already exists."

    def __init__(self):
        super().__init__(self.MESSAGE)
