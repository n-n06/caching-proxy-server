from typing import TypedDict
from enum import Enum

class CacheStatus(str, Enum):
    HIT = "HIT"
    MISS = "MISS"
    UNKNOWN = "UNKNOWN"

class LogMessage(TypedDict):
    method: str
    path: str
    status_code: int
    cache_status: CacheStatus
    duration_ms: float
    request_size: int | None
    response_size: int
    timestamp: float
