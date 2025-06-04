import pytest

from bot.resource.cog.validator.name_validator import NameValidator

NAME: str = "Clemou Delta"
COMPOSED_NAME: str = "Clemou-Delta"
TOO_LONG_NAME: str = "Jean-Pierre Alexandre-François de la Fontaine"
EMPTY_NAME: str = ""
CAMEL_CASE_NAME: str = "clemou delta"
CAMEL_CASE_COMPOSED_NAME: str = "clemou-delta"
UPPER_CASE_NAME: str = "CLEMOU DELTA"
UPPER_CASE_COMPOSED_NAME: str = "CLEMOU-DELTA"


@pytest.fixture
def name_validator() -> NameValidator:
    return NameValidator()


def test__when_using_valid_name__then_return_true(name_validator):
    assert name_validator.validate(NAME)


def test_when_using_composed_name__then_return_true(name_validator):
    assert name_validator.validate(COMPOSED_NAME)


def test__when_using_too_long_name__then_return_false(name_validator):
    assert not name_validator.validate(TOO_LONG_NAME)


def test__when_using_empty_name__then_return_false(name_validator):
    assert not name_validator.validate(EMPTY_NAME)


def test__when_using_camel_case_name__then_return_false(name_validator):
    assert not name_validator.validate(CAMEL_CASE_NAME)


def test__when_using_camel_composed_name__then_return_false(name_validator):
    assert not name_validator.validate(CAMEL_CASE_COMPOSED_NAME)


def test__when_using_upper_case_name__then_return_false(name_validator):
    assert not name_validator.validate(UPPER_CASE_NAME)


def test__when_using_upper_composed_name__then_return_false(name_validator):
    assert not name_validator.validate(UPPER_CASE_COMPOSED_NAME)
