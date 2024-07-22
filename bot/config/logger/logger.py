import logging
import os

from bot.config.logger.log import Log


class Logger:

    VERSION: int = 2
    LOGGER_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    NAME: str = "BuggyBotLogger"
    DIRECTORY: str = "log"

    def __init__(self, log_file: str, level=logging.DEBUG):
        self.__create_log_directory()
        logger_file_path = f"{self.DIRECTORY}/{log_file}"

        self.__logger = logging.getLogger(self.NAME)
        self.__logger.setLevel(level)

        file_handler = logging.FileHandler(logger_file_path, encoding="utf-8")
        console_handler = logging.StreamHandler()

        file_handler.setLevel(level)
        console_handler.setLevel(level)

        file_format = logging.Formatter(self.LOGGER_FORMAT)
        console_format = logging.Formatter(self.LOGGER_FORMAT)
        file_handler.setFormatter(file_format)
        console_handler.setFormatter(console_format)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(console_handler)

    def __create_log_directory(self):
        os.makedirs(self.DIRECTORY, exist_ok=True)

    def __log(self, level: int, message: str, method: str, exception: Exception = None):
        log: str = Log(self.VERSION, message, method, exception).to_json()
        self.__logger.log(level, log)

    def debug(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.INFO, message, method, exception)

    def info(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.INFO, message, method, exception)

    def warning(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.WARNING, message, method, exception)

    def error(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.ERROR, message, method, exception)

    def critical(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.CRITICAL, message, method, exception)

    def fatal(self, message: str, method: str, exception: Exception = None):
        self.__log(logging.FATAL, message, method, exception)
