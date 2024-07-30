from typing import Dict

from bot.config.exception.mapper_not_found_exception import (
    MapperNotFoundException,
)


class ExceptionMapper:
    __exception_mapper: Dict[type, str] = {}

    @classmethod
    def register(cls, exception_to_handle: type, exception_reply: str):
        if exception_to_handle in cls.__exception_mapper:
            raise RuntimeError(
                f"L'exception {exception_to_handle.__name__} est déjà prise en charge."
            )
        cls.__exception_mapper[exception_to_handle] = exception_reply

    @classmethod
    def get_response(cls, exception_class: type) -> str:
        if exception_class in cls.__exception_mapper:
            return cls.__exception_mapper[exception_class]

        for exception_type, response in cls.__exception_mapper.items():
            if issubclass(exception_class, exception_type):
                return response

        raise MapperNotFoundException(exception_class)

    @classmethod
    def clear(cls):
        cls.__exception_mapper.clear()
