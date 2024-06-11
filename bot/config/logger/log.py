import json
import string


class Log:
    version: int
    message: str

    def __init__(self, version: int, message: str):
        self.version = version
        self.message = message

    def to_dict(self) -> dict:
        return {"version": self.version, "message": self.message}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
