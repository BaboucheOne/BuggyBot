from bot.config.exception.exception_handler import ExceptionHandler


class InvalidFormatExceptionHandler(ExceptionHandler):
    def __init__(self):
        super().__init__(InvalidFormatExceptionHandler)

    def response(self) -> str:
        return "bad format"
