import re


class NameValidator:

    REGEX_PATTERN: str = r"^(?=.{1,40}$)([A-Z][a-z]+)([- ][A-Z][a-z]+)*$"

    def __init__(self):
        pass

    def validate(self, name: str):
        return bool(re.match(self.REGEX_PATTERN, name))
