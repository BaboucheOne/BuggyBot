class MissingProgramCodeException(Exception):

    MESSAGE = "The provided program code is missing.\nMake sure that the format is corresponding to B-GLO, B-IFT, B-IIG, C-IFT."

    def __init__(self):
        super().__init__(self.MESSAGE)
