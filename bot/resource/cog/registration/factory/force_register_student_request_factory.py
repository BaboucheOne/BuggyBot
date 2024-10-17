from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.force_register_student_request import (
    ForceRegisterStudentRequest,
)
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class ForceRegisterStudentRequestFactory(RequestFactory):
    REQUIRED_ARGUMENTS = 2

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

    def create(self, content: str) -> ForceRegisterStudentRequest:
        ni, member_discord_id = self._get_arguments(content)
        return ForceRegisterStudentRequest(
            SanitizerUtility.sanitize_ni(ni), int(member_discord_id)
        )
