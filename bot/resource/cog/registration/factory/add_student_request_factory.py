import re

from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class AddStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 4

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

    def __remove_extra_spaces(self, input_string: str) -> str:
        return re.sub(r"\s+", " ", input_string).strip()

    def create(self, content: str) -> AddStudentRequest:
        ni, firstname, lastname, program = self._get_arguments(content)
        return AddStudentRequest(
            SanitizerUtility.sanitize_ni(ni),
            self.__remove_extra_spaces(firstname),
            self.__remove_extra_spaces(lastname),
            program,
        )
