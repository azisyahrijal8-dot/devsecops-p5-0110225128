import pytest

from app.validators import validate_priority, validate_title


def test_title_valid_is_stripped():
    assert validate_title("  Belajar CI/CD ") == "Belajar CI/CD"


@pytest.mark.parametrize("bad", ["", "   ", None])
def test_title_empty_rejected(bad):
    with pytest.raises(ValueError):
        validate_title(bad)


def test_title_too_long():
    with pytest.raises(ValueError):
        validate_title("a" * 101)


def test_priority_normalized():
    assert validate_priority("HIGH") == "high"


def test_priority_invalid():
    with pytest.raises(ValueError):
        validate_priority("urgent")