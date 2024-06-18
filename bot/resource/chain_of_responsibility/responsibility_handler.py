from abc import abstractmethod

from bot.resource.chain_of_responsibility.responsibility import Responsibility


class ResponsibilityHandler(Responsibility):

    def __init__(self):
        self.__next_handler: ResponsibilityHandler | None = None

    def set_next(self, handler: Responsibility):
        self.__next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self.__next_handler:
            return self.__next_handler.handle(request)

        return request
