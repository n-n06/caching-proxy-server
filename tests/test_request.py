import requests

def test_request():
    data = requests.get("localhost:3000/45456/full")
    assert data != None
