import asyncio
from abc import abstractmethod, ABC
from typing import Callable


class Task(ABC):
    def __init__(self, schedule_method: Callable):
        self.__schedule_method = schedule_method

    def schedule(self):
        self.__schedule_method(self.__execute_async, asyncio.get_running_loop())

    def __execute_async(self, loop):
        asyncio.run_coroutine_threadsafe(self.do(), loop)

    @abstractmethod
    async def do(self):
        pass
