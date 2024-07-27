from typing import Dict


class ExceptionHandlerLocator:
    __exception_handlers: Dict[Exception, any] = {}

    @classmethod
    def register_handler(cls, exception_class: Exception, exception_handler):
        if exception_class in cls.__exception_handlers:
            raise RuntimeError(
                f"Exception {exception_class.__name__} already have an handler."
            )
        cls.__exception_handlers[exception_class] = exception_handler

    @classmethod
    def get_handler(cls, exception_class: Exception):
        if exception_class not in cls.__exception_handlers:
            raise RuntimeError(f"Exception {exception_class.__name__} has no handler.")
        return cls.__exception_handlers[exception_class]

    @classmethod
    def clear(cls):
        cls.__exception_handlers.clear()
