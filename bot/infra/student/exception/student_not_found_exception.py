class StudentNotFoundException(Exception):

    MESSAGE = "Student not found."

    def __init__(self):
        super().__init__(self.MESSAGE)
