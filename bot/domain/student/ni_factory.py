from bot.domain.student.attributs.ni import NI


class NIFactory:
    def __init__(self):
        pass

    def create(self, ni: str) -> NI:
        return NI(value=int(ni))
