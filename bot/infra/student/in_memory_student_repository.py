import copy
from typing import List

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.assembler.student_assembler import StudentAssembler
from bot.infra.student.exception.cannot_add_student_exception import (
    CannotAddStudentException,
)
from bot.infra.student.exception.cannot_unregister_student_exception import (
    CannotUnregisterStudentException,
)
from bot.infra.student.exception.cannot_update_student_exception import (
    CannotUpdateStudentException,
)
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.infra.student.exception.cannot_register_student_exception import (
    CannotRegisterStudentException,
)


class InMemoryStudentRepository(StudentRepository):

    def __init__(self, student_collection: List[Student]):
        self.__student_collection: List[Student] = student_collection
        self.__student_assembler: StudentAssembler = StudentAssembler()
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def find_student_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> Student:
        for student in self.__student_collection:
            if student.discord_user_id.value == discord_user_id.value:
                return copy.deepcopy(student)
        raise StudentNotFoundException(discord_id=discord_user_id)

    def find_students_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> List[Student]:
        found_students = [
            copy.deepcopy(student)
            for student in self.__student_collection
            if student.discord_user_id.value == discord_user_id.value
        ]
        return found_students

    def find_student_by_ni(self, ni: NI) -> Student:
        for student in self.__student_collection:
            if student.ni.value == ni.value:
                return copy.deepcopy(student)
        raise StudentNotFoundException(ni=ni)

    def add_student(self, student: Student):
        if any(s.ni.value == student.ni.value for s in self.__student_collection):
            raise CannotAddStudentException(student)
        self.__student_collection.append(student)
        self.__logger.info(
            f"L'étudiant {repr(student)} a bien été ajouté à la base de données.",
            method="add_student",
        )

    def update_student(self, student: Student):
        for idx, existing_student in enumerate(self.__student_collection):
            if existing_student.ni.value == student.ni.value:
                self.__student_collection[idx] = student
                self.__logger.info(
                    f"{repr(student)} a bien été mis à jour dans la base de données.",
                    method="update_student",
                )
                return
        raise CannotUpdateStudentException(student)

    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        for student in self.__student_collection:
            if student.ni.value == ni.value:
                student.discord_user_id = discord_user_id
                self.__logger.info(
                    f"L'étudiant {repr(ni)} {repr(discord_user_id)} a bien été enregistré.",
                    method="register_student",
                )
                return
        raise CannotRegisterStudentException(ni)

    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        for student in self.__student_collection:
            if student.ni.value == ni.value:
                student.discord_user_id = DiscordUserId(
                    DiscordUserId.INVALID_DISCORD_ID
                )
                self.__logger.info(
                    f"L'étudiant {repr(ni)} {repr(discord_user_id)} en cache a bien été désenregistré.",
                    method="unregister_student",
                )
                return
        raise CannotUnregisterStudentException(ni)
