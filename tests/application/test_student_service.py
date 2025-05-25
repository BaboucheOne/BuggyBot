import pytest

from unittest.mock import MagicMock, AsyncMock, patch

from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
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
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.infra.student.in_memory_student_repository import InMemoryStudentRepository
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest
from bot.resource.cog.registration.request.force_register_student_request import (
    ForceRegisterStudentRequest,
)
from bot.resource.cog.registration.request.force_unregister_student_request import (
    ForceUnregisterStudentRequest,
)
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)
from bot.resource.cog.registration.request.unregister_student_request import (
    UnregisterStudentRequest,
)
from bot.resource.exception.user_not_in_server_exception import UserNotInServerException

A_BAC_NAME: str = "B-GLO"
A_STUDENT_FIRSTNAME: str = "Jack"
A_STUDENT_LASTNAME: str = "Black"

A_NI: str = "123456789"
ANOTHER_NI: str = "987654321"
A_DISCORD_ID: int = 123456789012749572
ANOTHER_DISCORD_ID: int = 944456689012749572
AN_INVALID_DISCORD_ID: int = -1


def given_unregistered_student(ni: str) -> Student:
    return Student(
        NI(value=int(ni)),
        Firstname(value=A_STUDENT_FIRSTNAME),
        Lastname(value=A_STUDENT_LASTNAME),
        ProgramCode(value=A_BAC_NAME),
        DiscordUserId(value=AN_INVALID_DISCORD_ID),
    )


def given_registered_student(ni: str, discord_user_id: int) -> Student:
    return Student(
        NI(value=int(ni)),
        Firstname(value=A_STUDENT_FIRSTNAME),
        Lastname(value=A_STUDENT_LASTNAME),
        ProgramCode(value=A_BAC_NAME),
        DiscordUserId(value=discord_user_id),
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
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])

    student_service: StudentService = StudentService(student_repository)

    request: AddStudentRequest = AddStudentRequest(
        A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_BAC_NAME
    )

    await student_service.add_student(request)


@pytest.mark.asyncio
async def test__given_registered_student__when_add_same_student__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    request: AddStudentRequest = AddStudentRequest(
        A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_BAC_NAME
    )

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.add_student(request)


@pytest.mark.asyncio
async def test__given_a_student__when_add_already_existing_student__then_student_already_exists_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    a_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository([a_student])

    student_service: StudentService = StudentService(student_repository)

    request: AddStudentRequest = AddStudentRequest(
        A_NI, A_STUDENT_FIRSTNAME, A_STUDENT_LASTNAME, A_BAC_NAME
    )

    with pytest.raises(StudentAlreadyExistsException):
        await student_service.add_student(request)


@pytest.mark.asyncio
async def test__given_unregistered_student__when_register_student__then_student_is_registered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    register_request: RegisterStudentRequest = RegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    await student_service.register_student(register_request)


@pytest.mark.asyncio
async def test__given_unregistered_student__when_force_register_student__then_student_is_registered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    request: ForceRegisterStudentRequest = ForceRegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        await student_service.force_register_student(request)


@pytest.mark.asyncio
async def test__given_unregistered_student_and_discord_user_id_not_on_server__when_force_register_student__then_user_not_in_server_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    request: ForceRegisterStudentRequest = ForceRegisterStudentRequest(
        A_NI, ANOTHER_DISCORD_ID
    )

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = False

        with pytest.raises(UserNotInServerException):
            await student_service.force_register_student(request)


@pytest.mark.asyncio
async def test__given_no_students__when_force_register_student__then_student_not_found(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])

    student_service: StudentService = StudentService(student_repository)

    request: ForceRegisterStudentRequest = ForceRegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        with pytest.raises(StudentNotFoundException):
            await student_service.force_register_student(request)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_force_register_student__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    register_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [register_student]
    )

    student_service: StudentService = StudentService(student_repository)

    request: ForceRegisterStudentRequest = ForceRegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        with pytest.raises(StudentAlreadyRegisteredException):
            await student_service.force_register_student(request)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_force_register_with_same_discord_client_id__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    register_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    unregistered_student: Student = given_unregistered_student(ANOTHER_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [register_student, unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    request: ForceRegisterStudentRequest = ForceRegisterStudentRequest(
        ANOTHER_NI, A_DISCORD_ID
    )

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        with pytest.raises(StudentAlreadyRegisteredException):
            await student_service.force_register_student(request)


@pytest.mark.asyncio
async def test__given_already_registered_student__when_register_with_same_discord_client_id__then_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    unregistered_student: Student = given_unregistered_student(ANOTHER_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student, unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    register_request: RegisterStudentRequest = RegisterStudentRequest(
        ANOTHER_NI, A_DISCORD_ID
    )

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.register_student(register_request)


@pytest.mark.asyncio
async def test__given_no_students_and_unregistered_student__when_register_student__then_student_not_found_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    student_repository: StudentRepository = InMemoryStudentRepository([])
    student_service: StudentService = StudentService(student_repository)

    register_request: RegisterStudentRequest = RegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    with pytest.raises(StudentNotFoundException):
        await student_service.register_student(register_request)


@pytest.mark.asyncio
async def test__given_registered_student__when_register_student__then_raise_student_already_registered_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)

    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)

    register_request: RegisterStudentRequest = RegisterStudentRequest(
        A_NI, A_DISCORD_ID
    )

    with pytest.raises(StudentAlreadyRegisteredException):
        await student_service.register_student(register_request)


@pytest.mark.asyncio
async def test__given_registered_student__when_unregister_student__then_student_is_unregistered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    request: UnregisterStudentRequest = UnregisterStudentRequest(A_DISCORD_ID)

    await student_service.unregister_student(request)

    student_service.notify_on_student_unregistered.assert_awaited_once_with(
        DiscordUserId(value=A_DISCORD_ID)
    )


@pytest.mark.asyncio
async def test__given_unregistered_student__when_unregister_student__then_student_not_found_exception(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    unregistered_student: Student = given_unregistered_student(A_NI)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [unregistered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    request: UnregisterStudentRequest = UnregisterStudentRequest(A_DISCORD_ID)

    with pytest.raises(StudentNotFoundException):
        await student_service.unregister_student(request)


@pytest.mark.asyncio
async def test__given_registered_student__when_force_unregister_student__then_student_is_unregistered(
    setup_and_teardown_dependencies,
):
    logger_mock = MagicMock(spec=Logger)
    ServiceLocator.register_dependency(Logger, logger_mock)

    registered_student: Student = given_registered_student(A_NI, A_DISCORD_ID)
    student_repository: StudentRepository = InMemoryStudentRepository(
        [registered_student]
    )

    student_service: StudentService = StudentService(student_repository)
    student_service.notify_on_student_unregistered = AsyncMock()

    request: ForceUnregisterStudentRequest = ForceUnregisterStudentRequest(A_NI)

    await student_service.force_unregister_student(request)

    with patch(
        "bot.domain.utility.Utility.does_user_exist_on_server"
    ) as mock_does_user_exist_on_server:
        mock_does_user_exist_on_server.return_value = True

        student_service.notify_on_student_unregistered.assert_awaited_once_with(
            DiscordUserId(value=A_DISCORD_ID)
        )
