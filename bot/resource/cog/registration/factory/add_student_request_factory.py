from bot.resource.chain_of_responsibility.responsibility_handler import (
    ResponsibilityHandler,
)
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest


class AddStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 5

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        super().__init__(self.REQUIRED_ARGUMENTS)
        self.__ni_sanitizer = ni_sanitizer

    def create(self, content: str) -> AddStudentRequest:
        ni, firstname, lastname, program, new_admitted = self._get_arguments(content)
        return AddStudentRequest(
            self.__ni_sanitizer.handle(ni), firstname, lastname, program, new_admitted
        )
