import os
import pytest
from caching_proxy_server import cli
from click.testing import CliRunner

@pytest.fixture
def runner():
    return CliRunner()

def test_clear_cache(runner):
    result = runner.invoke(cli.cli, ["--clear-cache"])
    
    # assert result.exit_code == 0
    assert not os.path.exists('cache.pkl')
