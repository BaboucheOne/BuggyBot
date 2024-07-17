from typing import List, Dict

from pymongo.collection import Collection

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.constants import StudentMongoDbKey
from bot.infra.student.assembler.student_assembler import StudentAssembler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.infra.student.exception.student_not_registered_exception import (
    StudentNotRegisteredException,
)


class MongoDbStudentRepository(StudentRepository):

    def __init__(self, student_collection: Collection):
        self.__student_collection: Collection = student_collection
        self.__student_assembler: StudentAssembler = StudentAssembler()

        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def find_student_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> Student:
        student_response: Dict = self.__student_collection.find_one(
            {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        )

        if not student_response:
            self.__logger.info(
                f"find_student_by_discord_user_id - "
                f"L'étudiant avec {repr(discord_user_id)} n'a pas été trouvé."
            )
            raise StudentNotFoundException()

        return self.__student_assembler.from_json(student_response)

    def find_students_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> List[Student]:
        students = self.__student_collection.find(
            {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        )
        return [self.__student_assembler.from_dict(student) for student in students]

    def find_student_by_ni(self, ni: NI) -> Student:
        query = {StudentMongoDbKey.NI: ni.value}
        student_response: Dict = self.__student_collection.find_one(query)

        if not student_response:
            self.__logger.info(
                f"find_student_by_ni - "
                f"L'étudiant avec {repr(ni)} n'a pas été trouvé."
            )
            raise StudentNotFoundException()

        return self.__student_assembler.from_json(student_response)

    def add_student(self, student: Student):
        student_dict = self.__student_assembler.to_dict(student)
        self.__student_collection.insert_one(student_dict)

    def update_student(self, student: Student):
        student_dict = self.__student_assembler.to_dict(student)
        filter_query = {StudentMongoDbKey.NI: student.ni.value}
        update_query = {"$set": student_dict}

        self.__student_collection.update_one(filter_query, update_query)

    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        filter_query = {StudentMongoDbKey.NI: ni.value}
        update_query = {
            "$set": {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        }
        result = self.__student_collection.update_one(filter_query, update_query)

        if result.modified_count == 0:
            self.__logger.info(
                f"register_student - "
                f"L'utilisateur avec {repr(ni)}, {repr(discord_user_id)} "
                f"n'a pas pu être enregistré dans la base de données."
            )
            raise StudentNotRegisteredException()

    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        filter_query = {StudentMongoDbKey.NI: ni.value}
        update_query = {
            "$set": {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        }
        self.__student_collection.update_one(filter_query, update_query)
