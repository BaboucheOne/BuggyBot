import pytest

from bot.resource.cog.validators.ni_validator import NIValidator

NI: str = "111222333"
INVALID_DIGIT_LEN_NI: str = "11122233"
NON_DIGIT_NI: str = "abcdefghi"
LETTER_AND_DIGIT_NI: str = "123abc456"


@pytest.fixture
def ni_validator() -> NIValidator:
    return NIValidator()


def test__when_validate_valid_ni__should_return_true(ni_validator):
    assert ni_validator.validate(NI)


def test__when_validate_invalid_length_ni__should_return_false(ni_validator):
    assert not ni_validator.validate(INVALID_DIGIT_LEN_NI)


def test__when_validate_non_digit_ni_should__return_false(ni_validator):
    assert not ni_validator.validate(NON_DIGIT_NI)


def test__when_validate_letter_and_digit_ni__should_return_false(ni_validator):
    assert not ni_validator.validate(LETTER_AND_DIGIT_NI)
