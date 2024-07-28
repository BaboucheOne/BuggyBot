from bot.config.exception.exception_handler import ExceptionHandler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class StudentNotFoundExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(StudentNotFoundException)

    def response(self) -> str:
        return "Student not found"
