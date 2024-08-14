class ForceUnregisterStudentRequest:

    def __init__(self, ni: str):
        self.ni = ni

    def __repr__(self) -> str:
        return f"ForceUnregisterStudentRequest({self.ni})"
