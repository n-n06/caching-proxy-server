import unittest
import pytest

from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests
import requests_mock 

from click.testing import CliRunner

from caching_proxy_server import cli




@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200
    response.headers = {'Content-Type': 'application/json'}
    response.content = b'{"key": "value"}'
    return response

class TestImplementation(TestCase):
    API_URL = "http://localhost:3000"

    @requests_mock.mock()
    def test_cache_response(self, mock_for_requests, runner):
        unittest.
        runner.invoke(cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"])
        
        #mocking your request(s)
        expected_headers1 = {'X-Cache': 'MISS'}
        expected_headers2 =  {'X-Cache': 'HIT'}

        # expected = 'some_text'
        mock_for_requests.get(TestImplementation.API_URL + "/v4/anime/37987/full", headers=expected_headers1)

        #running your code with requests
        response1 = requests.get(TestImplementation.API_URL + "/v4/anime/37987/full")

        #comparing output
        self.assertEqual(response1.headers, expected_headers1)

        mock_for_requests.get(TestImplementation.API_URL + "/v4/anime/37987/full", headers=expected_headers2)

        response2 = requests.get(TestImplementation.API_URL +  "/v4/anime/37987/full")

        self.assertEqual(response2.headers, expected_headers2)
        # self.assertEqual(response.text, expected)

    @requests_mock.mock()
    def test_no_cache_hit_on_first_request(self, mock_for_requests, runner):
        expected_headers1 = {'X-Cache': 'MISS'}

        runner.invoke(cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"])
        mock_for_requests.get(TestImplementation.API_URL + "/v4/anime/33352/full", headers=expected_headers1)

        #running your code with requests
        response1 = requests.get(TestImplementation.API_URL + "/v4/anime/33352/full")

        #comparing output
        self.assertEqual(response1.headers, expected_headers1)






# def test_cache_response(runner, mock_response):
#     with patch("requests.get") as mock_get:
#         mock_get.return_value = mock_response
#
#         runner.invoke(cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"])
#
#         response1 = requests.get("http://localhost:3000/v4/anime/23273/full")
#         assert response1.headers.get("X-Cache") == "MISS"
#
#         response2 = requests.get("http://localhost:3000/v4/anime/23273/full")
#         assert response2.headers.get("X-Cache") == "HIT"
#
#         mock_get.assert_called_once_with("https://api.jikan.moe/23273/full")
#
#         raise KeyboardInterrupt
#         sys.exit(0)

# def test_no_cache_hit_on_first_request(runner, mock_response):
#     with patch("requests.get") as mock_get:
#         mock_get.return_value = mock_response
#
#         runner.invoke(cli.cli, ["--port", "3000", "--origin", "https://api.jikan.moe"])
#         response = requests.get("http://localhost:3000/v4/anime/33352/full")
#         print(response.headers)
#
#         assert response.headers.get("X-Cache") == "MISS"
#
#         raise KeyboardInterrupt
#         sys.exit(0)
