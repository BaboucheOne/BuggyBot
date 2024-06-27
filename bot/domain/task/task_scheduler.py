import threading
import time
from typing import List

import schedule

from bot.domain.task.task import Task


class TaskScheduler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__stop_event = threading.Event()

    def add_tasks(self, tasks: List[Task]):
        for task in tasks:
            task.schedule()

    def run(self) -> None:
        while not self.__stop_event.is_set():
            schedule.run_pending()
            time.sleep(1.0)

    def stop(self):
        self.__stop_event.set()
