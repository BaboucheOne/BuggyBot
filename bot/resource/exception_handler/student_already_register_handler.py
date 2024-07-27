from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
from bot.resource.constants import ReplyMessage
from bot.resource.exception_handler.exception_handler import ExceptionHandler


class NotFoundExceptionMapper(ExceptionHandler):
    def __init__(self):
        super().__init__(self, StudentAlreadyRegisteredException)

    def response(self) -> str:
        return ReplyMessage.ALREADY_REGISTERED
