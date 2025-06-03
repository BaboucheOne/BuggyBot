import re


class NameValidator:

    REGEX_PATTERN: str = (
        r"^(?=.{1,40}$)([A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ]+)([- ][A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ]+)*$"
    )

    def __init__(self):
        pass

    def validate(self, name: str):
        return bool(re.match(self.REGEX_PATTERN, name))
