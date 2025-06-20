from prometheus_client import (
        Counter, Histogram, Gauge
)

PROMETHEUS_PORT = 8000

REQUEST_HANDLER = Counter(
    'proxy_requests_total',
    'Total number of requests',
    ['method', 'cache', 'status']
)

REQUEST_DURATION = Histogram(
    'proxy_request_duration',
    'Request duration in ms',
    ['cache']
)

CACHE_HIT_RATIO = Gauge(
    'proxy_cache_hit_ratio',
    'Ratio of cache hits to total GET requests'
)

UP = Gauge(
    'proxy_up',
    '1 if the proxy server is running, 0 otherwise'
)

REQUEST_SIZE = Histogram(
    'proxy_request_size_bytes',
    'Size of incoming requests',
    buckets=(100, 500, 1000, 5000, 10000, 50000)
)

RESPONSE_SIZE = Histogram(
    'proxy_response_size_bytes',
    'Size of outgoing responses',
    buckets=(100, 500, 1000, 5000, 10000, 50000)
)
