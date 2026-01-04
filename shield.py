# shield.py

import time

# Rate-limit configuration (v1 – locked)
WINDOW_SECONDS = 60
MAX_REQUESTS = 30

# In-memory state
# key: client_id
# value: [count, window_start]
RATE_STATE = {}


def check_rate(client_id: str) -> bool:
    now = time.time()
    record = RATE_STATE.get(client_id)

    if not record:
        RATE_STATE[client_id] = [1, now]
        return True

    count, start = record

    # Reset window
    if now - start > WINDOW_SECONDS:
        RATE_STATE[client_id] = [1, now]
        return True

    # Exceeded limit
    if count >= MAX_REQUESTS:
        return False

    # Increment within window
    RATE_STATE[client_id][0] += 1
    return True
