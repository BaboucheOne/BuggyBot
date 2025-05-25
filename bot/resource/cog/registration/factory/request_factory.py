from abc import ABC, abstractmethod
from typing import Tuple, List

from bot.resource.exception.missing_arguments_exception import MissingArgumentsException


class RequestFactory(ABC):
    def __init__(self, number_of_arguments):
        self._number_of_arguments = number_of_arguments

    def __strip_arguments(self, arguments: List[str]) -> List[str]:
        return [argument.strip() for argument in arguments]

    @abstractmethod
    def _validate_arguments(self, content: str) -> Tuple[any, ...] or any:
        pass

    def _get_arguments(self, content: str) -> Tuple[any, ...] or any:
        content = content.rstrip()
        arguments = content.split(",", self._number_of_arguments - 1)

        if len(arguments) != self._number_of_arguments:
            raise MissingArgumentsException(self._number_of_arguments)

        arguments = self.__strip_arguments(arguments)

        if len(arguments) == 1:
            return arguments[0]
        return tuple(arguments)
