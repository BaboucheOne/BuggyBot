from abc import ABC
from typing import Tuple

from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException


class RequestFactory(ABC):
    def __init__(self, number_of_arguments):
        self._number_of_arguments = number_of_arguments

    def _get_arguments(self, content: str) -> Tuple[any, ...] or any:
        content = content.rstrip()
        arguments = content.split(" ", self._number_of_arguments - 1)

        if len(arguments) != self._number_of_arguments:
            raise MissingArgumentsException(self._number_of_arguments)

        if len(arguments) == 1:
            return arguments[0]
        return tuple(arguments)
