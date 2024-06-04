from dataclasses import dataclass


@dataclass
class NewAdmitted:
    value: bool

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"NewAdmitted({str(self.value)})"
