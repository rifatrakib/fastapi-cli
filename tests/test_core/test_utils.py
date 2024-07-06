import json
from unittest.mock import mock_open, patch

from server.core.utils import read_secrets


def test_read_secrets_with_default_mode():
    secrets = {"key1": "value1", "key2": "value2"}
    # Mock open to simulate reading a file with secrets
    with patch("builtins.open", mock_open(read_data=json.dumps(secrets))):
        with patch("os.getenv", return_value="development"):  # Mock environment variable
            result = read_secrets("development")
            assert result == secrets


def test_read_secrets_with_custom_mode():
    secrets = {"key1": "value1", "key2": "value2"}
    # Mock open to simulate reading a file with secrets
    with patch("builtins.open", mock_open(read_data=json.dumps(secrets))):
        with patch("os.getenv", return_value="custom_mode"):  # Mock environment variable
            result = read_secrets("custom_mode")
            assert result == secrets


def test_read_secrets_file_not_found():
    # Mock open to simulate a file not found scenario
    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = FileNotFoundError
        with patch("os.getenv", return_value="nonexistent_mode"):  # Mock environment variable
            result = read_secrets("nonexistent_mode")
            assert result == {}


def test_read_secrets_json_decode_error():
    # Mock open to simulate a file with invalid JSON
    with patch("builtins.open", mock_open(read_data="{invalid_json")):
        with patch("os.getenv", return_value="development"):  # Mock environment variable
            result = read_secrets("development")
            assert result == {}
