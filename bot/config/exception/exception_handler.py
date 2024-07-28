import abc


class ExceptionHandler(abc.ABC):
    def __init__(self, exception_to_handle: type):
        self.__exception_to_handle = exception_to_handle

    @property
    def exception_to_handle(self) -> type:
        return self.__exception_to_handle

    @abc.abstractmethod
    def response(self) -> str:
        pass
