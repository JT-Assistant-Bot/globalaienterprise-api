import time
import threading

# In-memory key store
# key -> { "credits": int, "created_at": float }
API_KEYS = {}

LOCK = threading.Lock()

# -----------------------------
# MANUAL TEST KEY (TEMPORARY)
# -----------------------------
# This key is ONLY for verification.
# You can remove it after testing.
API_KEYS["TEST-KEY-123"] = {
    "credits": 1000,
    "created_at": time.time(),
}

# -----------------------------
# CORE FUNCTIONS
# -----------------------------

def is_valid_key(api_key: str) -> bool:
    with LOCK:
        return api_key in API_KEYS


def has_credits(api_key: str) -> bool:
    with LOCK:
        return API_KEYS.get(api_key, {}).get("credits", 0) > 0


def consume_credit(api_key: str) -> bool:
    with LOCK:
        if api_key not in API_KEYS:
            return False
        if API_KEYS[api_key]["credits"] <= 0:
            return False
        API_KEYS[api_key]["credits"] -= 1
        return True


def grant_credits(api_key: str, amount: int):
    with LOCK:
        if api_key not in API_KEYS:
            API_KEYS[api_key] = {
                "credits": amount,
                "created_at": time.time(),
            }
        else:
            API_KEYS[api_key]["credits"] += amount


def get_key_info(api_key: str):
    with LOCK:
        return API_KEYS.get(api_key)
