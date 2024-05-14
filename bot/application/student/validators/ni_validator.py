class NIValidator:

    NI_DIGITS_COUNT = 9

    def __init__(self):
        pass

    def validate(self, ni: str) -> bool:
        return len(ni) is self.NI_DIGITS_COUNT
