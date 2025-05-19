import pytest

from unittest.mock import MagicMock, AsyncMock, patch

from discord import Member

from bot.application.student.student_service import StudentService
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)
from bot.resource.cog.registration.request.unregister_student_request import (
    UnregisterStudentRequest,
)

A_STUDENT_FIRSTNAME: Firstname = Firstname(value="Jack")
A_STUDENT_LASTNAME = Lastname(value="Black")

A_NI: str = "123456789"
A_DISCORD_ID: int = 123456789012749572
AN_INVALID_DISCORD_ID: int = -1

UNREGISTERED_STUDENT: Student = Student(
    NI(value=int(A_NI)),
    A_STUDENT_FIRSTNAME,
    A_STUDENT_LASTNAME,
    ProgramCode(value="GLO"),
    DiscordUserId(value=AN_INVALID_DISCORD_ID),
)

REGISTERED_STUDENT: Student = Student(
    NI(value=int(A_NI)),
    A_STUDENT_FIRSTNAME,
    A_STUDENT_LASTNAME,
    ProgramCode(value="GLO"),
    DiscordUserId(value=A_DISCORD_ID),
)


@pytest.fixture
def setup_and_teardown_dependencies():
    yield

    ServiceLocator.clear()


@pytest.mark.asyncio
async def test__given_unregistered_student__when_register_student__then_student_is_registered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository = MagicMock(spec=StudentRepository)
    student_repository.find_student_by_ni.return_value = UNREGISTERED_STUDENT
    student_repository.find_students_by_discord_user_id.return_value = []
    student_repository.register_student = MagicMock()

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_registered = AsyncMock()

    register_request: RegisterStudentRequest = RegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    await student_service.register_student(register_request)

    excepted_ni: NI = NI(value=int(A_NI))
    excepted_discord_user_id: DiscordUserId = DiscordUserId(value=A_DISCORD_ID)

    student_repository.register_student.assert_called_with(
        excepted_ni, excepted_discord_user_id
    )
    student_service.notify_on_student_registered.assert_awaited_once_with(excepted_ni)


@pytest.mark.asyncio
async def test__given_registered_student__when_unregister_student__then_student_is_unregistered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository = MagicMock(spec=StudentRepository)
    student_repository.find_student_by_discord_user_id.return_value = REGISTERED_STUDENT
    student_repository.find_students_by_discord_user_id.return_value = [
        REGISTERED_STUDENT
    ]
    student_repository.unregister_student = MagicMock()

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    request: UnregisterStudentRequest = UnregisterStudentRequest(A_DISCORD_ID)

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        await student_service.unregister_student(request)

        student_repository.unregister_student.assert_called_with(
            NI(value=int(A_NI)), DiscordUserId(value=AN_INVALID_DISCORD_ID)
        )
        student_service.notify_on_student_unregistered.assert_awaited_once_with(
            DiscordUserId(value=A_DISCORD_ID)
        )


@pytest.mark.asyncio
async def test__given__member__when_remove_member__then_member_is_removed(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository = MagicMock(spec=StudentRepository)
    student_repository.unregister_student = MagicMock()

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_member_removed = AsyncMock()

    member = MagicMock(spec=Member)
    member.id.return_value = A_DISCORD_ID

    await student_service.remove_member(member)

    student_repository.unregister_student(
        NI(value=int(A_NI)), DiscordUserId(value=AN_INVALID_DISCORD_ID)
    )
    student_service.notify_on_member_removed.assert_awaited_once_with(member)
