import os
import pickle
import signal
import atexit
import cachetools


class CacheHandler:

    CACHE_FILE = 'cache.pkl'

    def __init__(self, maxsize : float = 1024*1024, expire : int = 3600):
        self.cache = self.load_cache(maxsize, expire)

    def load_cache(self, maxsize : float, expire : int):
        try:
            with open(self.CACHE_FILE, 'rb') as f:
                cache = pickle.load(f)
        except FileNotFoundError:
            cache = cachetools.TTLCache(maxsize, expire)
        return cache

    def save_cache(self):
        with open(self.CACHE_FILE, 'wb') as f:
            pickle.dump(self.cache, f)

    def set(self, key, value):
        self.cache[key] = value;

    def get(self, key):
        try:
            return self.cache[key]
        except KeyError:
            return None

    def clear(self):
        os.remove('cache.pkl')
        self.cache.clear()

    def handle_exit(self, sig, frame):
        self.save_cache()
        exit(0)



