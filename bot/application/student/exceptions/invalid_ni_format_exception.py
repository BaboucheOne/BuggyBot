from typing import Union

from bot.domain.student.attribut.ni import NI


class InvalidNIFormatException(RuntimeError):
    NI_UNION = Union[NI, int]

    MESSAGE = "%s does not match the format."

    def __init__(self, ni: NI_UNION):
        super().__init__(self.MESSAGE % repr(ni))
