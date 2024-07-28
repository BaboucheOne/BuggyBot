from bot.config.exception.exception_handler import ExceptionHandler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.resource.constants import ReplyMessage


class StudentNotFoundExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(StudentNotFoundException)

    def response(self) -> str:
        return ReplyMessage.STUDENT_NOT_FOUND
