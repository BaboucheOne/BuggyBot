from typing import Union

from bot.application.student.exceptions.invalid_format_exception import (
    InvalidFormatException,
)
from bot.domain.student.attribut.ni import NI


class InvalidNIFormatException(InvalidFormatException):
    NI_UNION = Union[NI, int]

    MESSAGE = "%s ne correspond pas au format."

    def __init__(self, ni: NI_UNION):
        super().__init__(self.MESSAGE % repr(ni))
