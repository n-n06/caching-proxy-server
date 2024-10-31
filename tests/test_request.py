import requests

def test_request():
    data = requests.get("localhost:3000/v4/anime/45456/full")
    
    data = requests.get("localhost:3000/v4/anime/45456/full")
    assert data.headers.get('X-Cache') == 'HIT'
