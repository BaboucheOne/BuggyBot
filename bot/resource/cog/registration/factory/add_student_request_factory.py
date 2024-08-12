import re

from bot.resource.chain_of_responsibility.responsibility_handler import (
    ResponsibilityHandler,
)
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest


class AddStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 4

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        super().__init__(self.REQUIRED_ARGUMENTS)
        self.__ni_sanitizer = ni_sanitizer

    def __remove_extra_spaces(self, input_string: str) -> str:
        return re.sub(r"\s+", " ", input_string).strip()

    def create(self, content: str) -> AddStudentRequest:
        ni, firstname, lastname, program = self._get_arguments(content)
        return AddStudentRequest(
            self.__ni_sanitizer.handle(ni),
            self.__remove_extra_spaces(firstname),
            self.__remove_extra_spaces(lastname),
            program,
        )
