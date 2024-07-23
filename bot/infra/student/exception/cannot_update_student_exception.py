from bot.domain.student.student import Student
from bot.infra.student.exception.mongo_fail_operation_exception import (
    MongoFailOperationException,
)


class CannotUpdateStudentException(MongoFailOperationException):

    MESSAGE = "L'étudiant %s n'a pas été mis à jour dans la base de données."

    def __init__(self, student: Student):
        super().__init__(self.MESSAGE % repr(student))
