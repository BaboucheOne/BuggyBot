import re


class SanitizerUtility:

    ONLY_KEEP_DIGITS_REGEX: str = r"\D"

    @staticmethod
    def sanitize_ni(ni: str) -> str:
        return re.sub(SanitizerUtility.ONLY_KEEP_DIGITS_REGEX, "", ni)
