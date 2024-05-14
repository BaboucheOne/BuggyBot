from pymongo.collection import Collection

from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI
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

    def find_student_by_ni(self, ni: NI) -> Student:
        query = {StudentMongoDbKey.NI: ni.value}
        student_response = self.__student_collection.find_one(query)

        if not student_response:
            raise StudentNotFoundException()

        return self.__student_assembler.from_json(student_response)

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
            raise StudentNotRegisteredException()
