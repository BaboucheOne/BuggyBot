from bot.resource.constants import ReplyMessage
from bot.resource.exception_handler.exception_handler import ExceptionHandler


class GenericHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(self, Exception)

    def response(self) -> str:
        return ReplyMessage.UNSUCCESSFUL_GENERIC
