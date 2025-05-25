from bot.domain.student.attribut.ni import NI


class ForceUnregisterStudentRequest:

    def __init__(self, ni: NI):
        self.ni = ni

    def __repr__(self) -> str:
        return f"ForceUnregisterStudentRequest({self.ni})"
