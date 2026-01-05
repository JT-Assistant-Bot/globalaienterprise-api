# shield.py

import time
from typing import Dict

# ==============================
# CONFIG (LOCKED)
# ==============================

WINDOW_SECONDS = 60
MAX_REQUESTS = 30

# Temporary valid keys (manual monetization v1)
# Replace / extend only after first payment
VALID_API_KEYS = {
    "PAID_KEY_001": "active",
}

PAYMENT_INSTRUCTION = (
    "Access denied. This endpoint requires a paid API key.\n"
    "To obtain access, contact the operator and request a Shield API key."
)

# ==============================
# IN-MEMORY STATE
# ==============================

# key: api_key
# value: [count, window_start]
RATE_STATE: Dict[str, list] = {}


# ==============================
# CORE LOGIC
# ==============================

def check_shield(api_key: str) -> bool:
    """
    Returns True if request is allowed.
    Returns False if blocked (rate limit or unpaid).
    """

    # 1. Hard block if no key
    if not api_key:
        return False

    # 2. Hard block if unpaid / invalid key
    if api_key not in VALID_API_KEYS:
        return False

    now = time.time()
    record = RATE_STATE.get(api_key)

    # 3. First request
    if not record:
        RATE_STATE[api_key] = [1, now]
        return True

    count, start = record

    # 4. Reset window
    if now - start > WINDOW_SECONDS:
        RATE_STATE[api_key] = [1, now]
        return True

    # 5. Rate limit exceeded
    if count >= MAX_REQUESTS:
        return False

    # 6. Increment within window
    RATE_STATE[api_key][0] += 1
    return True


def shield_response(api_key: str):
    """
    Unified helper for HTTP handlers.
    Returns (allowed: bool, message: str)
    """

    allowed = check_shield(api_key)

    if not allowed:
        if not api_key or api_key not in VALID_API_KEYS:
            return False, PAYMENT_INSTRUCTION
        return False, "Rate limit exceeded. Try again later."

    return True, "OK"
