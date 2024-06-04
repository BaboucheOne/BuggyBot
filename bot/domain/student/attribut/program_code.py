from dataclasses import dataclass


@dataclass
class ProgramCode:
    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"ProgramCode({str(self.value)})"
