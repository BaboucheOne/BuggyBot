from typing import Union

from bot.domain.student.attribut.program_code import ProgramCode


class MissingProgramCodeException(Exception):
    PROGRAM_UNION = Union[ProgramCode, str]

    MESSAGE = "Le code programme fourni %s n'existe pas."

    def __init__(self, program_code: PROGRAM_UNION):
        super().__init__(self.MESSAGE % repr(program_code))
