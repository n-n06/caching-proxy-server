
import pytest
from unittest.mock import patch, MagicMock
import requests
from caching_proxy_server import cli
from click.testing import CliRunner

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

def test_cache_response(runner, mock_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        runner.invoke(cli.cli, ["--port", "3000", "--origin", "http://dummyjson.com"])
        requests.get("http://localhost:3000/v4/anime/23273/full")
        response = requests.get("http://localhost:3000/products")

        mock_get.assert_called_once_with("http://dummyjson.com/products")
        assert response.headers.get("X-Cache") == "HIT"

def test_no_cache_hit_on_first_request(runner, mock_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        runner.invoke(cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"])
        response = requests.get("http://localhost:3000/v4/anime/23273/full")

        assert response.headers.get("X-Cache") == "MISS"
