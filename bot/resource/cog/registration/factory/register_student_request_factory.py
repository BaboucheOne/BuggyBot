from typing import Tuple

from bot.application.student.exceptions.invalid_ni_format_exception import (
    InvalidNIFormatException,
)
from bot.resource.cog.validators.ni_validator import NIValidator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.factory.ni_factory import NIFactory
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class RegisterStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 1

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

        self.__ni_validator = NIValidator()

        self.__ni_factory: NIFactory = NIFactory()

    def _validate_arguments(self, content: str) -> Tuple[any, ...] or any:
        ni = self._get_arguments(content)

        ni = SanitizerUtility.sanitize_ni(ni)

        if not self.__ni_validator.validate(ni):
            raise InvalidNIFormatException(ni)

        return ni

    def create(self, content: str, author_id: int) -> RegisterStudentRequest:
        ni = self._validate_arguments(content)
        return RegisterStudentRequest(
            self.__ni_factory.create(ni), DiscordUserId(author_id)
        )
