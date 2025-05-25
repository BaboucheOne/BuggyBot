from typing import Tuple

from bot.application.student.exceptions.invalid_discord_id_format_exception import (
    InvalidDiscordIdFormatException,
)
from bot.application.student.exceptions.invalid_ni_format_exception import (
    InvalidNIFormatException,
)
from bot.application.student.validators.discord_id_validator import DiscordIdValidator
from bot.application.student.validators.ni_validator import NIValidator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.factory.ni_factory import NIFactory
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.force_register_student_request import (
    ForceRegisterStudentRequest,
)
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class ForceRegisterStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 2

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

        self.__ni_validator: NIValidator = NIValidator()
        self.__discord_id_validator: DiscordIdValidator = DiscordIdValidator()

        self.__ni_factory: NIFactory = NIFactory()

    def _validate_arguments(self, content: str) -> Tuple[any, ...] or any:
        ni, member_discord_id = self._get_arguments(content)

        ni = SanitizerUtility.sanitize_ni(ni)
        if not self.__ni_validator.validate(ni):
            raise InvalidNIFormatException(ni)

        if not self.__discord_id_validator.validate(member_discord_id):
            raise InvalidDiscordIdFormatException(member_discord_id)

        return ni, member_discord_id

    def create(self, content: str) -> ForceRegisterStudentRequest:
        ni, member_discord_id = self._validate_arguments(content)
        return ForceRegisterStudentRequest(
            self.__ni_factory.create(ni), DiscordUserId(member_discord_id)
        )
