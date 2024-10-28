from time import sleep

from caching_proxy_server.cache_handler import CacheHandler

def test_set_cache_key():
    c = CacheHandler(2)

    c.set("https://someurl.com/users", {"status" : 200})

    assert c.get("https://someurl.com/users") == {"status" : 200} 

    sleep(2)

    assert c.get("https://someurl.com/users") == None
