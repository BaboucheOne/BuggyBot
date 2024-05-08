from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class MongoDbStudentRepository(StudentRepository):

    def __init__(self, student_collection):
        self.student_collection = student_collection

    def get_student_by_ni(self, ni: int) -> Student:
        query = {"ni": ni}
        student_response = self.student_collection.find_one(query)

        if not student_response:
            raise StudentNotFoundException()

        return Student(
            ni=student_response["ni"],
            lastname=student_response["lastname"],
            firstname=student_response["firstname"],
            program_code=student_response["program_code"],
            new=student_response["new"],
            discord_user_id=student_response["discord_user_id"],
        )
