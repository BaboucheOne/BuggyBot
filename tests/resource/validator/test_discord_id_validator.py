import pytest

from bot.resource.cog.validator.discord_id_validator import DiscordIdValidator

DISCORD_ID: int = 123456789012749572
OLD_DISCORD_ID: int = 1234567891023567
INVALID_LENGTH_DISCORD_ID: int = 2133


@pytest.fixture
def discord_id_validator() -> DiscordIdValidator:
    return DiscordIdValidator()


def test__when_using_old_discord_id__then_return_true(discord_id_validator):
    assert not discord_id_validator.validate(OLD_DISCORD_ID)


def test__when_using_discord_id__then_return_true(discord_id_validator):
    assert discord_id_validator.validate(DISCORD_ID)


def test__when_using_invalid_length_discord_id__then_return_false(discord_id_validator):
    assert not discord_id_validator.validate(INVALID_LENGTH_DISCORD_ID)
