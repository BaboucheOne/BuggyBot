from bot.cog.chain_of_responsibility.responsibility_handler import ResponsibilityHandler
from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException
from bot.cog.request.add_student_request import AddStudentRequest


class AddStudentRequestFactory:

    REQUIRED_ARGUMENTS = 5

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        self.__ni_sanitizer = ni_sanitizer

    def create(self, content: str) -> AddStudentRequest:
        arguments = content.split(" ")

        if len(arguments) != self.REQUIRED_ARGUMENTS:
            raise MissingArgumentsException(self.REQUIRED_ARGUMENTS)

        ni = self.__ni_sanitizer.handle(arguments[0].strip())
        firstname = arguments[1].strip()
        lastname = arguments[2].strip()
        program = arguments[3].strip()
        new_admitted = arguments[4].strip()

        return AddStudentRequest(ni, firstname, lastname, program, new_admitted)
