from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class NI(JsonSchemaMixin):
    value: int

    def __eq__(self, other):
        if isinstance(other, NI):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)
