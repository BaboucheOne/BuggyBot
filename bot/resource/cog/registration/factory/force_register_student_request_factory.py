from bot.resource.chain_of_responsibility.responsibility_handler import (
    ResponsibilityHandler,
)
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.force_register_student_request import (
    ForceRegisterStudentRequest,
)


class ForceRegisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 2

    def __init__(self, ni_sanitizer: ResponsibilityHandler):
        super().__init__(self.REQUIRED_ARGUMENTS)
        self.__ni_sanitizer = ni_sanitizer

    def create(self, content: str) -> ForceRegisterStudentRequest:
        ni, member_discord_id = self._get_arguments(content)
        return ForceRegisterStudentRequest(
            self.__ni_sanitizer.handle(ni), int(member_discord_id)
        )
