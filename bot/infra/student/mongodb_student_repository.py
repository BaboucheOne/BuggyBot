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
from bot.infra.student.exception.cannot_register_student_exception import (
    CannotRegisterStudentException,
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
            raise StudentNotFoundException(discord_id=discord_user_id)

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
            raise StudentNotFoundException(ni=ni)

        return self.__student_assembler.from_json(student_response)

    def add_student(self, student: Student):
        student_dict = self.__student_assembler.to_dict(student)
        self.__student_collection.insert_one(student_dict)

        self.__logger.info(
            f"L'étudiant {repr(student)} a bien été ajouté à la base de données.",
            method="add_student",
        )

    def update_student(self, student: Student):
        student_dict = self.__student_assembler.to_dict(student)
        filter_query = {StudentMongoDbKey.NI: student.ni.value}
        update_query = {"$set": student_dict}

        self.__student_collection.update_one(filter_query, update_query)

        self.__logger.info(
            f"{repr(student)} a bien été mis à jour dans la base de données.",
            method="update_student",
        )

    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        filter_query = {StudentMongoDbKey.NI: ni.value}
        update_query = {
            "$set": {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        }
        result = self.__student_collection.update_one(filter_query, update_query)

        if result.modified_count == 0:
            raise CannotRegisterStudentException(ni)

        self.__logger.info(
            f"L'étudiant {repr(ni)} {repr(discord_user_id)} a bien été enregistré.",
            method="register_student",
        )

    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        filter_query = {StudentMongoDbKey.NI: ni.value}
        update_query = {
            "$set": {StudentMongoDbKey.DISCORD_USER_ID: discord_user_id.value}
        }
        self.__student_collection.update_one(filter_query, update_query)

        self.__logger.info(
            f"L'étudiant {repr(ni)} {repr(discord_user_id)} en cache a bien été désenregistré.",
            method="unregister_student",
        )
