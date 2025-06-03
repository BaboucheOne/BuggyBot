import pytest

from unittest.mock import MagicMock, AsyncMock

from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
from bot.application.student.student_service import StudentService
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.infra.student.in_memory_student_repository import InMemoryStudentRepository
from bot.resource.exception.user_not_in_server_exception import UserNotInServerException

A_PROGRAM_CODE: ProgramCode = ProgramCode("B-GLO")
A_STUDENT_FIRSTNAME: Firstname = Firstname("Jack")
A_STUDENT_LASTNAME: Lastname = Lastname("Black")

A_NI: NI = NI(123456789)
ANOTHER_NI: NI = NI(987654321)
A_DISCORD_ID: DiscordUserId = DiscordUserId(123456789012749572)
ANOTHER_DISCORD_ID: DiscordUserId = DiscordUserId(944456689012749572)
AN_INVALID_DISCORD_ID: DiscordUserId = DiscordUserId(-1)


def given_unregistered_student(ni: NI) -> Student:
    return Student(
        ni,
        A_STUDENT_FIRSTNAME,
        A_STUDENT_LASTNAME,
        A_PROGRAM_CODE,
        AN_INVALID_DISCORD_ID,
    )


def given_registered_student(ni: NI, discord_user_id: DiscordUserId) -> Student:
    return Student(
        ni,
        A_STUDENT_FIRSTNAME,
        A_STUDENT_LASTNAME,
        A_PROGRAM_CODE,
        discord_user_id,
    )


@pytest.fixture
def setup_and_teardown_dependencies():
    yield

    ServiceLocator.clear()


@pytest.mark.asyncio
async def test__given_no_students__when_add_student__then_student_is_added(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])

    student_service: StudentService = StudentService(student_repository)

    await student_service.add_student(
        A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_PROGRAM_CODE
    )


@pytest.mark.asyncio
async def test__given_registered_student__when_add_same_student__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.add_student(
            A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_PROGRAM_CODE
        )


@pytest.mark.asyncio
async def test__given_a_student__when_add_already_existing_student__then_student_already_exists_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    a_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository([a_student])

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyExistsException):
        await student_service.add_student(
            A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_PROGRAM_CODE
        )


@pytest.mark.asyncio
async def test__given_unregistered_student__when_register_student__then_student_is_registered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    await student_service.register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_unregistered_student__when_force_register_student__then_student_is_registered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = True
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    await student_service.force_register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_unregistered_student_and_discord_user_id_not_on_server__when_force_register_student__then_user_not_in_server_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = False
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(UserNotInServerException):
        await student_service.force_register_student(A_NI, ANOTHER_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_no_students__when_force_register_student__then_student_not_found(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = True
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentNotFoundException):
        await student_service.force_register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_force_register_student__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = True
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    register_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [register_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.force_register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_force_register_with_same_discord_client_id__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = True
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    register_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    unregistered_student: Student = given_unregistered_student(ANOTHER_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [register_student, unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.force_register_student(ANOTHER_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_register_with_same_discord_client_id__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    unregistered_student: Student = given_unregistered_student(ANOTHER_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student, unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.register_student(ANOTHER_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_no_students_and_unregistered_student__when_register_student__then_student_not_found_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])
    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentNotFoundException):
        await student_service.register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_registered_student__when_register_student__then_raise_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)

    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.register_student(A_NI, A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_registered_student__when_unregister_student__then_student_is_unregistered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    await student_service.unregister_student(A_DISCORD_ID)

    student_service.notify_on_student_unregistered.assert_awaited_once_with(
        A_DISCORD_ID
    )


@pytest.mark.asyncio
async def test__given_unregistered_student__when_unregister_student__then_student_not_found_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    with pytest.raises(StudentNotFoundException):
        await student_service.unregister_student(A_DISCORD_ID)


@pytest.mark.asyncio
async def test__given_registered_student__when_force_unregister_student__then_student_is_unregistered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    discord_client_mock = MagicMock(spec=DiscordClient)
    discord_client_mock.does_user_exists.return_value = True
    ServiceLocator.register_dependency(Logger, logger_mock)
    ServiceLocator.register_dependency(DiscordClient, discord_client_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    await student_service.force_unregister_student(A_NI)

    student_service.notify_on_student_unregistered.assert_awaited_once_with(
        A_DISCORD_ID
    )
