from dataclasses import dataclass


@dataclass
class Lastname:
    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Lastname({str(self.value)})"
