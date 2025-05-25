import re
from typing import Tuple

from bot.application.student.exceptions.invalid_name_format_exception import (
    InvalidNameFormatException,
)
from bot.application.student.exceptions.invalid_ni_format_exception import (
    InvalidNIFormatException,
)
from bot.application.student.exceptions.missing_program_code_exception import (
    MissingProgramCodeException,
)
from bot.application.student.validators.discord_id_validator import DiscordIdValidator
from bot.application.student.validators.name_validator import NameValidator
from bot.application.student.validators.ni_validator import NIValidator
from bot.application.student.validators.program_code_validator import (
    ProgramCodeValidator,
)
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.factory.ni_factory import NIFactory
from bot.resource.cog.registration.factory.request_factory import RequestFactory
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest
from bot.resource.utility.sanitizer_utility import SanitizerUtility


class AddStudentRequestFactory(RequestFactory):

    REQUIRED_ARGUMENTS = 4

    def __init__(self):
        super().__init__(self.REQUIRED_ARGUMENTS)

        self.__ni_validator: NIValidator = NIValidator()
        self.__name_validator: NameValidator = NameValidator()
        self.__discord_id_validator: DiscordIdValidator = DiscordIdValidator()
        self.__program_code_validator: ProgramCodeValidator = ProgramCodeValidator()

        self.__ni_factory: NIFactory = NIFactory()

    def __remove_extra_spaces(self, input_string: str) -> str:
        return re.sub(r"\s+", " ", input_string).strip()

    def _validate_arguments(self, content: str) -> Tuple[any, ...] or any:
        ni, firstname, lastname, program_code = self._get_arguments(content)

        ni = SanitizerUtility.sanitize_ni(ni)
        firstname = self.__remove_extra_spaces(firstname)
        lastname = self.__remove_extra_spaces(lastname)

        if not self.__ni_validator.validate(ni):
            raise InvalidNIFormatException(ni)

        if not self.__name_validator.validate(firstname):
            raise InvalidNameFormatException(firstname)

        if not self.__name_validator.validate(lastname):
            raise InvalidNameFormatException(lastname)

        if not self.__program_code_validator.validate(program_code):
            raise MissingProgramCodeException(program_code)

        return ni, firstname, lastname, program_code

    def create(self, content: str) -> AddStudentRequest:
        ni, firstname, lastname, program_code = self._validate_arguments(content)

        return AddStudentRequest(
            self.__ni_factory.create(ni),
            Firstname(firstname),
            Lastname(lastname),
            ProgramCode(program_code.upper()),
        )
