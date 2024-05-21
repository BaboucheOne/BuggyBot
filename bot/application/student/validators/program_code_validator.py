from bot.domain.constants import UniProgram


class ProgramCodeValidator:

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
