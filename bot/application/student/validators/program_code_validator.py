from bot.domain.constants import UniProgram


class ProgramCodeValidator:

    PROGRAMS = {
        UniProgram.GLO,
        UniProgram.IFT,
        UniProgram.IIG,
        UniProgram.CERTIFICATE,
        UniProgram.HONORIFIQUE,
    }

    def __init__(self):
        pass

    def validate(self, program: str) -> bool:
        return program in self.PROGRAMS
