from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
from bot.resource.constants import ReplyMessage
from bot.config.exception.exception_handler import ExceptionHandler


class StudentAlreadyRegisteredExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(StudentAlreadyRegisteredException)

    def response(self) -> str:
        return ReplyMessage.ALREADY_REGISTERED
