from bot.resource.chain_of_responsibility.responsibility_handler import (
    ResponsibilityHandler,
)
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)


class RegisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 1

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        super().__init__(self.REQUIRED_ARGUMENTS)
        self.__ni_sanitizer = ni_sanitizer

    def create(self, content: str, author_id: int) -> RegisterStudentRequest:
        ni = self._get_arguments(content)
        return RegisterStudentRequest(self.__ni_sanitizer.handle(ni), author_id)
