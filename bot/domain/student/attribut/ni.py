from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class NI(JsonSchemaMixin):
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"NI({str(self.value)})"

    def __eq__(self, other):
        if not isinstance(other, NI):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
