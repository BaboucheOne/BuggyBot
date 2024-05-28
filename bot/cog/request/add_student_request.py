class AddStudentRequest:

    def __init__(
        self,
        ni: str,
        firstname: str,
        lastname: str,
        program_code: str,
        new_admitted: str,
    ):
        self.ni = ni
        self.firstname = firstname
        self.lastname = lastname
        self.program_code = program_code
        self.new_admitted = new_admitted
