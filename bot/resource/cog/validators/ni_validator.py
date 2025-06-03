class NIValidator:

    NI_DIGITS_COUNT = 9

    def __init__(self):
        pass

    def validate(self, ni: str) -> bool:
        return len(ni) == self.NI_DIGITS_COUNT and ni.isdigit()
