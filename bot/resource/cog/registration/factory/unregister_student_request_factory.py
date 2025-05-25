from typing import Tuple

from bot.application.student.exceptions.invalid_discord_id_format_exception import (
    InvalidDiscordIdFormatException,
)
from bot.application.student.validators.discord_id_validator import DiscordIdValidator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.unregister_student_request import (
    UnregisterStudentRequest,
)


class UnregisterStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 1

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

        self.__discord_id_validator: DiscordIdValidator = DiscordIdValidator()

    def _validate_arguments(self, content: str) -> Tuple[any, ...] or any:
        discord_id = self._get_arguments(content)

        if not self.__discord_id_validator.validate(discord_id):
            raise InvalidDiscordIdFormatException(discord_id)

        return discord_id

    def create(self, content: str) -> UnregisterStudentRequest:
        discord_id = self._validate_arguments(content)
        return UnregisterStudentRequest(DiscordUserId(discord_id))
