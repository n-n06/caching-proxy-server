from .metrics import (
    CACHE_HIT_RATIO, REQUEST_DURATION, REQUEST_HANDLER, 
    REQUEST_SIZE, RESPONSE_SIZE, UP
)

_hit_count = 0
_total_get_reqs = 0

def inc_request(method, cache, status):
    print(f"Sending data to Prom - Method = {method} | Cache = {cache} | Status code = {status}")
    REQUEST_HANDLER.labels(method, cache, str(status)).inc()

def record_duration(cache, duration_ms):
    print(f"Sending duration = {duration_ms}ms to Prom")
    REQUEST_DURATION.labels(cache).observe(duration_ms)

def record_request_size(size_bytes):
    REQUEST_SIZE.observe(size_bytes)

def record_response_size(size_bytes):
    RESPONSE_SIZE.observe(size_bytes)

def update_cache_hit_ratio(hit):
    global _hit_count, _total_get_reqs

    if hit:
        _hit_count += 1
    _total_get_reqs += 1

    ratio = _hit_count / _total_get_reqs if _total_get_reqs > 0 else 0
    print("Prom hit ratio is %f", ratio)
    CACHE_HIT_RATIO.set(ratio)

def mark_proxy_up():
    UP.set(1)

def mark_proxy_down():
    UP.set(0)
