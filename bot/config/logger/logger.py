import logging

from bot.config.logger.log import Log


class Logger:

    VERSION: int = 1
    LOGGER_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    NAME: str = "BuggyBotLogger"

    def __init__(self, log_file: str, level=logging.DEBUG):
        self.logger = logging.getLogger(self.NAME)
        self.logger.setLevel(level)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        console_handler = logging.StreamHandler()

        file_handler.setLevel(level)
        console_handler.setLevel(level)

        file_format = logging.Formatter(self.LOGGER_FORMAT)
        console_format = logging.Formatter(self.LOGGER_FORMAT)
        file_handler.setFormatter(file_format)
        console_handler.setFormatter(console_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def __create_log(self, message: str) -> str:
        return Log(self.VERSION, message).to_json()

    def debug(self, message):
        log_message = self.__create_log(message)
        self.logger.debug(log_message)

    def info(self, message):
        log_message = self.__create_log(message)
        self.logger.info(log_message)

    def warning(self, message):
        log_message = self.__create_log(message)
        self.logger.warning(log_message)

    def error(self, message):
        log_message = self.__create_log(message)
        self.logger.error(log_message)

    def critical(self, message):
        log_message = self.__create_log(message)
        self.logger.critical(log_message)

    def fatal(self, message):
        log_message = self.__create_log(message)
        self.logger.fatal(log_message)
