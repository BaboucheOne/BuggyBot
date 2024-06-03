from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.cache.cache_repository import CacheRepository


class CachedStudentRepository(StudentRepository, CacheRepository):

    def __init__(self, repository: StudentRepository):
        super().__init__()
        self.__repository = repository

    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        self._set_dirty(ni)
        self.__repository.register_student(ni, discord_user_id)

    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        self._set_dirty(ni)
        self.__repository.unregister_student(ni, discord_user_id)

    def add_student(self, student: Student):
        self.__repository.add_student(student)

    def update_student(self, student: Student):
        self._set_dirty(student.ni)
        self.__repository.update_student(student)

    def find_student_by_ni(self, ni: NI) -> Student:
        if self._is_cached(ni) and not self._is_dirty(ni):
            return self._get_cached_item(ni).data

        student = self.__repository.find_student_by_ni(ni)
        self._set_cached_item(ni, student)
        return student
