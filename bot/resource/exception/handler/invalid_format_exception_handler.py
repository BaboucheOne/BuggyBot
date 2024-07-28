from bot.config.exception.exception_handler import ExceptionHandler
from bot.resource.constants import ReplyMessage


class InvalidFormatExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(InvalidFormatExceptionHandler)

    def response(self) -> str:
        return ReplyMessage.INVALID_FORMAT
