from bot.cog.chain_of_responsibility.responsibility_handler import ResponsibilityHandler
from bot.cog.registration.factory.request_factory import RequestFactory
from bot.cog.request.unregister_student_request import UnregisterStudentRequest


class UnregisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 1

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        super().__init__(self.REQUIRED_ARGUMENTS)
        self.__ni_sanitizer = ni_sanitizer

    def create(self, content: str) -> UnregisterStudentRequest:
        ni = self._get_arguments(content)
        return UnregisterStudentRequest(self.__ni_sanitizer.handle(ni))
