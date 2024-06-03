from bot.domain.student.attribut.ni import NI


class NIFactory:
    def __init__(self):
        pass

    def create(self, ni: str) -> NI:
        return NI(value=int(ni))
