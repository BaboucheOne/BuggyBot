from bot.resource.exception_handler.exception_handler import ExceptionHandler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class StudentNotFoundHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(self, StudentNotFoundException)

    def response(self) -> str:
        return "Student not found"
