import json
from typing import Optional


class LogJsonKey:
    VERSION: str = "version"
    MESSAGE: str = "message"
    METHOD: str = "method"
    EXCEPTION: str = "exception"


class Log:
    version: int
    message: str

    def __init__(
        self,
        version: int,
        method: str,
        message: str,
        exception: Optional[Exception] = None,
    ):
        self.version = version
        self.message = message
        self.method = method
        self.exception = exception

    def to_dict(self) -> dict:
        log = {
            LogJsonKey.VERSION: self.version,
            LogJsonKey.METHOD: self.method,
            LogJsonKey.MESSAGE: self.message,
        }
        if self.exception:
            log[LogJsonKey.EXCEPTION] = type(self.exception).__name__
        return log

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
