from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.force_unregister_student_request import (
    ForceUnregisterStudentRequest,
)
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class ForceUnregisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 1

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

    def create(self, content: str) -> ForceUnregisterStudentRequest:
        ni = self._get_arguments(content)
        return ForceUnregisterStudentRequest(SanitizerUtility.sanitize_ni(ni))
