from abc import ABC
from typing import Tuple

from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException


class RequestFactory(ABC):
    def __init__(self, number_of_arguments):
        self._number_of_arguments = number_of_arguments

    def _get_arguments(self, content: str) -> Tuple:
        arguments = content.split(" ")

        if len(arguments) != self._number_of_arguments:
            raise MissingArgumentsException(self._number_of_arguments)

        return tuple(arguments)
