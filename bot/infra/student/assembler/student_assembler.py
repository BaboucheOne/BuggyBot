from typing import Dict

from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.firstname import Firstname
from bot.domain.student.attributs.lastname import Lastname
from bot.domain.student.attributs.new_admitted import NewAdmitted
from bot.domain.student.attributs.ni import NI
from bot.domain.student.attributs.program_code import ProgramCode
from bot.domain.student.student import Student
from bot.infra.constants import StudentMongoDbKey


class StudentAssembler:

    def from_json(self, student_json: Dict) -> Student:
        return Student(
            ni=NI(student_json[StudentMongoDbKey.NI]),
            firstname=Firstname(student_json[StudentMongoDbKey.FIRSTNAME]),
            lastname=Lastname(student_json[StudentMongoDbKey.LASTNAME]),
            program_code=ProgramCode(student_json[StudentMongoDbKey.PROGRAM_CODE]),
            new_admitted=NewAdmitted(student_json[StudentMongoDbKey.NEW_ADMITTED]),
            discord_user_id=DiscordUserId(
                student_json[StudentMongoDbKey.DISCORD_USER_ID]
            ),
        )

    def from_dict(self, entry: dict) -> Student:
        return Student(
            ni=NI(entry[StudentMongoDbKey.NI]),
            firstname=Firstname(entry[StudentMongoDbKey.FIRSTNAME]),
            lastname=Lastname(entry[StudentMongoDbKey.LASTNAME]),
            program_code=ProgramCode(entry[StudentMongoDbKey.PROGRAM_CODE]),
            new_admitted=NewAdmitted(entry[StudentMongoDbKey.NEW_ADMITTED]),
            discord_user_id=DiscordUserId(entry[StudentMongoDbKey.DISCORD_USER_ID]),
        )

    def to_dict(self, student: Student) -> Dict:
        return {
            StudentMongoDbKey.NI: student.ni.value,
            StudentMongoDbKey.FIRSTNAME: student.firstname.value,
            StudentMongoDbKey.LASTNAME: student.lastname.value,
            StudentMongoDbKey.PROGRAM_CODE: student.program_code.value,
            StudentMongoDbKey.NEW_ADMITTED: student.new_admitted.value,
            StudentMongoDbKey.DISCORD_USER_ID: student.discord_user_id.value,
        }
