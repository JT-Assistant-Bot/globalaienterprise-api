# shield.py

import time
from typing import Dict
from keys import check_and_consume

# ==============================
# CONFIG (LOCKED)
# ==============================

WINDOW_SECONDS = 60
MAX_REQUESTS = 30

PAYMENT_INSTRUCTION = (
    "Access denied. This endpoint requires a paid API key.\n"
    "Purchase API credits to obtain access."
)

# ==============================
# IN-MEMORY RATE STATE
# ==============================

# key: api_key
# value: [count, window_start]
RATE_STATE: Dict[str, list] = {}


# ==============================
# CORE SHIELD LOGIC
# ==============================

def shield_response(api_key: str):
    """
    Validates API key (paid) and enforces rate limit.
    Does NOT consume credits.
    """

    # 1. Missing key
    if not api_key:
        return False, PAYMENT_INSTRUCTION

    # 2. Validate key by attempting a dry credit check
    # We consume 1 credit and immediately restore it
    # because shield is a gate, not a usage endpoint
    valid = check_and_consume(api_key)
    if not valid:
        return False, PAYMENT_INSTRUCTION

    # Restore consumed credit (undo)
    # This is safe because keys.py is in-memory
    from keys import API_KEY_INDEX, ISSUED_KEYS
    identity = API_KEY_INDEX.get(api_key)
    if identity:
        ISSUED_KEYS[identity]["credits"] += 1

    now = time.time()
    record = RATE_STATE.get(api_key)

    # 3. First request
    if not record:
        RATE_STATE[api_key] = [1, now]
        return True, "OK"

    count, start = record

    # 4. Reset window
    if now - start > WINDOW_SECONDS:
        RATE_STATE[api_key] = [1, now]
        return True, "OK"

    # 5. Rate limit exceeded
    if count >= MAX_REQUESTS:
        return False, "Rate limit exceeded. Try again later."

    # 6. Increment within window
    RATE_STATE[api_key][0] += 1
    return True, "OK"
