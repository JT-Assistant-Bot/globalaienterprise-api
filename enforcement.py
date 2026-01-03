# enforcement.py

import time
from collections import defaultdict

# In-memory usage store (acceptable for zero-capital MVP)
# Structure:
# {
#   api_key: {
#       "count": int,
#       "reset_ts": epoch_seconds
#   }
# }
_usage_store = defaultdict(dict)

# Constants
FREE_TIER_LIMIT = 20
WINDOW_SECONDS = 86400  # 24 hours


def _current_ts():
    return int(time.time())


def check_and_increment(api_key: str) -> bool:
    """
    Returns True if request is allowed.
    Returns False if limit exceeded.
    """

    now = _current_ts()

    record = _usage_store.get(api_key)

    # First-time key or expired window
    if not record or now >= record.get("reset_ts", 0):
        _usage_store[api_key] = {
            "count": 1,
            "reset_ts": now + WINDOW_SECONDS
        }
        return True

    # Within active window
    if record["count"] < FREE_TIER_LIMIT:
        record["count"] += 1
        return True

    # Limit exceeded
    return False


def remaining_calls(api_key: str) -> int:
    """
    Returns remaining free calls for the current window.
    """
    record = _usage_store.get(api_key)

    if not record:
        return FREE_TIER_LIMIT

    return max(FREE_TIER_LIMIT - record["count"], 0)
