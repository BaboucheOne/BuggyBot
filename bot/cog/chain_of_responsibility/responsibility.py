from abc import ABC, abstractmethod


class Responsibility(ABC):
    @abstractmethod
    def set_next(self, handler: "Responsibility"):
        pass

    @abstractmethod
    def handle(self, request):
        pass
