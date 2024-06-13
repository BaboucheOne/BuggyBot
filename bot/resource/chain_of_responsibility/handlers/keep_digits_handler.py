import re

from bot.resource.chain_of_responsibility.responsibility_handler import (
    ResponsibilityHandler,
)


class KeepDigitsHandler(ResponsibilityHandler):
    ONLY_DIGIT_PATTERN_REGEX = r"\D"

    def __init__(self):
        super().__init__()

    def handle(self, request: str):
        digits = re.sub(self.ONLY_DIGIT_PATTERN_REGEX, "", request)
        return super().handle(digits)
