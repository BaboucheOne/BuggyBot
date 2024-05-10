from bot.domain.student.attributs.ni import NI
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.constants import StudentMongoDbKey
from bot.infra.student.assembler.student_assembler import StudentAssembler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class MongoDbStudentRepository(StudentRepository):

    def __init__(self, student_collection):
        self.student_collection = student_collection
        self.student_assembler = StudentAssembler()

    def get_student_by_ni(self, ni: NI) -> Student:
        query = {StudentMongoDbKey.NI: ni.value}
        student_response = self.student_collection.find_one(query)

        if not student_response:
            raise StudentNotFoundException()

        return self.student_assembler.from_json(student_response)

    def update_student(self, student: Student):
        student_dict = self.student_assembler.to_dict(student)
        filter_query = {StudentMongoDbKey.NI: student.ni.value}
        update_query = {"$set": student_dict}

        self.student_collection.update_one(filter_query, update_query)
