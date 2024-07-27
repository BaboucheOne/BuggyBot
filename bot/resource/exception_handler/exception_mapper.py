from bot.resource.exception_handler.exception_handler import ExceptionHandler
from bot.resource.exception_handler.exception_handler_locator import (
    ExceptionHandlerLocator,
)


class NotFoundException(RuntimeError):
    def __init__(self):
        super().__init__("Hello, I'm a runtime error")


class NotFoundExceptionMapper(ExceptionHandler):
    def __init__(self):
        super().__init__(self, NotFoundException)

    def response(self) -> str:
        return "I'm a returned response from the exception exception_handler."


if __name__ == "__main__":

    NotFoundExceptionMapper()

    try:
        raise NotFoundException()
    except BaseException as e:
        exception: ExceptionHandler = ExceptionHandlerLocator.get_handler(type(e))
        print(exception.response())
