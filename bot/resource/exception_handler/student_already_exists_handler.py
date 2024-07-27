from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.resource.constants import ReplyMessage
from bot.resource.exception_handler.exception_handler import ExceptionHandler


class StudentAlreadyExistsExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(self, StudentAlreadyExistsException)

    def response(self) -> str:
        return ReplyMessage.STUDENT_ALREADY_EXISTS
