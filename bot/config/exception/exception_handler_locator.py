from typing import Dict

from bot.config.exception.exception_handler import ExceptionHandler
from bot.config.exception.not_found_exception_handler import (
    NotFoundExceptionHandler,
)


class ExceptionHandlerLocator:
    __exception_handlers: Dict[type, ExceptionHandler] = {}

    @classmethod
    def register_handler(cls, exception_handler: ExceptionHandler):
        if exception_handler.exception_to_handle in cls.__exception_handlers:
            raise RuntimeError(
                f"Exception {exception_handler.exception_to_handle.__name__} already have an handler."
            )
        cls.__exception_handlers[exception_handler.exception_to_handle] = (
            exception_handler
        )

    @classmethod
    def get_handler(cls, exception_class: type) -> ExceptionHandler:
        if exception_class in cls.__exception_handlers:
            return cls.__exception_handlers[exception_class]

        for exception_type, handler in cls.__exception_handlers.items():
            if issubclass(exception_class, exception_type):
                return handler

        raise NotFoundExceptionHandler(exception_class)

    @classmethod
    def clear(cls):
        cls.__exception_handlers.clear()
