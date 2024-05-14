from tools.exception.name_too_long_exception import NameTooLongException


def check_name_overflow(name: str):
    if len(name) > 32:
        raise NameTooLongException()
