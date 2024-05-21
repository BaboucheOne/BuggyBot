from bot.domain.constants import UniProgram


class ProgramCodeValidator:

    NI_DIGITS_COUNT = 9
    PROGRAMS = {
        UniProgram.GLO,
        UniProgram.IFT,
        UniProgram.IIG,
        UniProgram.CERTIFICATE,
    }

    def __init__(self):
        pass

    def validate(self, program: str) -> bool:
        return program in {
            UniProgram.GLO,
            UniProgram.IFT,
            UniProgram.IIG,
            UniProgram.CERTIFICATE,
        }
