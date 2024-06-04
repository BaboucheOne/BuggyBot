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
        if isinstance(other, NI):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)
