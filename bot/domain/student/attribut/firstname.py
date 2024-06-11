from dataclasses import dataclass


@dataclass
class Firstname:
    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Firstname({str(self.value)})"
