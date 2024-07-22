class UnregisterStudentRequest:

    def __init__(self, ni: str):
        self.ni = ni

    def __repr__(self) -> str:
        return f"UnregisterStudentRequest({self.ni})"
