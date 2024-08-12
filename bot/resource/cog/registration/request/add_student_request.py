class AddStudentRequest:

    def __init__(self, ni: str, firstname: str, lastname: str, program_code: str):
        self.ni = ni
        self.firstname = firstname
        self.lastname = lastname
        self.program_code = program_code

    def __repr__(self) -> str:
        return (
            f"AddStudentRequest({self.ni}, {self.firstname}, {self.lastname}, "
            f"{self.program_code})"
        )
