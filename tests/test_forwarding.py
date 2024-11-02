import sys
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from caching_proxy_server import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response.content = b'{"key": "value"}'
    return response


def test_proxy_forwards_request(runner, mock_response, caplog):
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        with caplog.at_level("INFO"):
            result = runner.invoke(
                cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"]
            )

        # assert result.exit_code == 0
        assert "Server started on port" in caplog.text

        raise KeyboardInterrupt
