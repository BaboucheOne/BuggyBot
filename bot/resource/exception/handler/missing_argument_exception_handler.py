from bot.resource.constants import ReplyMessage
from bot.resource.exception.missing_arguments_exception import MissingArgumentsException
from bot.config.exception.exception_handler import ExceptionHandler


class MissingArgumentsExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(self, MissingArgumentsException)

    def response(self) -> str:
        return ReplyMessage.MISSING_ARGUMENTS_IN_COMMAND
