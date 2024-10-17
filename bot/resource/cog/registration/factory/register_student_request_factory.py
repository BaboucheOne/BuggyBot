from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class RegisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 1

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

    def create(self, content: str, author_id: int) -> RegisterStudentRequest:
        ni = self._get_arguments(content)
        return RegisterStudentRequest(SanitizerUtility.sanitize_ni(ni), author_id)
