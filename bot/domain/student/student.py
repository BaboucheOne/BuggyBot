from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Student(JsonSchemaMixin):
    ni: str
    firstname: str
    lastname: str
    program_code: str
    new: bool
    discord_user_id: int

    def is_registered(self) -> bool:
        return self.discord_user_id != -1

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.ni == other.ni
        return False

    def __hash__(self):
        return hash(self.ni)
