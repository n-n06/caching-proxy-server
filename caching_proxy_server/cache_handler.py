import cachetools

class CacheHandler:
    def __init__(self, expire : int):
        self.__cache = cachetools.TTLCache(1024*1024, expire)
    
    def set(self, key, value):
        self.__cache[key] = value;

    def get(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            return None

    def clear(self):
        self.__cache.clear()

