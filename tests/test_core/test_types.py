from datetime import datetime

from server.core.types import OptionalBoolean, OptionalDatetime, OptionalFloat, OptionalInteger, OptionalString


def test_optional_string():
    assert isinstance(None, OptionalString)
    assert isinstance("Hello", OptionalString)
    assert not isinstance(123, OptionalString)  # Should be False


def test_optional_integer():
    assert isinstance(None, OptionalInteger)
    assert isinstance(123, OptionalInteger)
    assert not isinstance("123", OptionalInteger)  # Should be False
    assert not isinstance(123.456, OptionalInteger)  # Should be False


def test_optional_float():
    assert isinstance(None, OptionalFloat)
    assert isinstance(123.456, OptionalFloat)
    assert not isinstance("123.456", OptionalFloat)  # Should be False
    assert not isinstance(123, OptionalFloat)  # Should be False


def test_optional_boolean():
    assert isinstance(None, OptionalBoolean)
    assert isinstance(True, OptionalBoolean)
    assert isinstance(False, OptionalBoolean)
    assert not isinstance("True", OptionalBoolean)  # Should be False
    assert not isinstance(1, OptionalBoolean)  # Should be False


def test_optional_datetime():
    assert isinstance(None, OptionalDatetime)
    assert isinstance(datetime.now(), OptionalDatetime)
    assert not isinstance("2024-07-05T12:30:00", OptionalDatetime)  # Should be False
    assert not isinstance(1234567890, OptionalDatetime)  # Should be False
