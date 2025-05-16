import pytest

from bot.application.student.validators.ni_validator import NIValidator


@pytest.fixture
def ni_validator():
    return NIValidator()

def test_ni_true(ni_validator):
    assert ni_validator.validate("111228454")
