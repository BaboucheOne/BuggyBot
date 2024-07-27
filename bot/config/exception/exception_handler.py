import abc

from bot.config.exception.exception_handler_locator import (
    ExceptionHandlerLocator,
)


class ExceptionHandler(abc.ABC):
    def __init__(self, handler: "ExceptionHandler", exception_to_handle: any):
        ExceptionHandlerLocator.register_handler(exception_to_handle, handler)

    @abc.abstractmethod
    def response(self) -> str:
        pass
