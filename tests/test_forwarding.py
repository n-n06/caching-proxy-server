
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
    response.headers = {'Content-Type': 'application/json'}
    response.json.return_value = {"key": "value"}
    return response

def test_proxy_forwards_request(runner, mock_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = runner.invoke(main.cli, ["--port", "3000", "--origin", "http://dummyjson.com"])

        assert result.exit_code == 0
        assert "Proxy server started" in result.output
