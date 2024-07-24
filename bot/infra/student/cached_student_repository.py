from typing import List

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.cache.cache_repository import CacheRepository
from bot.infra.cache.exception.cache_find_operation_not_found_exception import (
    CacheFindOperationNotFoundException,
)


class CachedStudentRepository(StudentRepository, CacheRepository):

    def __init__(self, repository: StudentRepository):
        super().__init__()
        self.__repository = repository
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def find_student_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> Student:
        try:
            return self._find_cache_item(
                lambda cache_item: cache_item.data.discord_user_id == discord_user_id
            )
        except CacheFindOperationNotFoundException:
            return self.__repository.find_student_by_discord_user_id(discord_user_id)

    def find_students_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> List[Student]:
        return self.__repository.find_students_by_discord_user_id(discord_user_id)

    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        self._set_dirty(ni)
        self.__logger.info(
            f"{repr(ni)} a bien été marqué comme sale.", method="update_student"
        )

        self.__repository.register_student(ni, discord_user_id)

    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        self._remove_cached_item(ni)
        self.__logger.info(
            f"{repr(ni)} a bien été retiré de la cache.", method="unregister_student"
        )

        self.__repository.unregister_student(ni, discord_user_id)

    def add_student(self, student: Student):
        self.__repository.add_student(student)

    def update_student(self, student: Student):
        self._set_dirty(student.ni)
        self.__logger.info(
            f"{repr(student)} a bien été marqué comme sale.", method="update_student"
        )
        self.__repository.update_student(student)

    def find_student_by_ni(self, ni: NI) -> Student:
        try:
            return self._find_cache_item(lambda cache_item: cache_item.data.ni == ni)
        except CacheFindOperationNotFoundException:
            student = self.__repository.find_student_by_ni(ni)
            self._set_cached_item(ni, student)

            self.__logger.info(
                f"L'étudiant {repr(student)} a bien été ajouté à la cache.",
                method="find_student_by_ni",
            )

            return student
