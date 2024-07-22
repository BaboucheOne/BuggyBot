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
        message: str,
        method: Optional[str] = None,
        exception: Optional[str] = None,
    ):
        self.version = version
        self.message = message
        self.method = method
        self.exception = exception

    def to_dict(self) -> dict:
        log = {LogJsonKey.VERSION: self.version, LogJsonKey.MESSAGE: self.message}
        if self.method:
            log[LogJsonKey.METHOD] = self.method
        if self.exception:
            log[LogJsonKey.EXCEPTION] = self.exception
        return log

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
