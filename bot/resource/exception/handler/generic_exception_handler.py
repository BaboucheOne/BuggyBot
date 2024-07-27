from bot.resource.constants import ReplyMessage
from bot.config.exception.exception_handler import ExceptionHandler


class GenericExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(self, Exception)

    def response(self) -> str:
        return ReplyMessage.UNSUCCESSFUL_GENERIC
