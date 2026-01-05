"""
keys.py
Central API key management for GlobalAIEnterprise.

This module MUST remain import-safe.
No side effects on import.
"""

from typing import Dict, Optional
import uuid
import threading

# -------------------------
# In-memory key store
# -------------------------
# NOTE:
# This is intentionally simple.
# Persistence will be added AFTER first revenue.

_LOCK = threading.Lock()

_KEYS: Dict[str, Dict] = {
    # Manual test key (for verification only)
    "TEST-KEY-123": {
        "credits": 999999,
        "email": "test@example.com",
        "license_key": "TEST",
    }
}


# -------------------------
# Core enforcement function
# -------------------------
def check_and_consume(api_key: Optional[str]) -> bool:
    """
    Validate API key and consume 1 credit.

    Returns:
        True  -> request allowed
        False -> request denied
    """
    if not api_key:
        return False

    with _LOCK:
        record = _KEYS.get(api_key)
        if not record:
            return False

        if record["credits"] <= 0:
            return False

        record["credits"] -= 1
        return True


# -------------------------
# Gumroad webhook support
# -------------------------
def create_paid_key(credits: int, email: str, license_key: str) -> str:
    """
    Create a new paid API key.

    Called from Gumroad webhook handler.
    """
    api_key = str(uuid.uuid4())

    with _LOCK:
        _KEYS[api_key] = {
            "credits": int(credits),
            "email": email,
            "license_key": license_key,
        }

    return api_key


# -------------------------
# Key lookup (optional helper)
# -------------------------
def get_key(email: str, license_key: str) -> Optional[Dict]:
    """
    Retrieve key metadata by email + license_key.
    """
    with _LOCK:
        for key, data in _KEYS.items():
            if data["email"] == email and data["license_key"] == license_key:
                return {
                    "api_key": key,
                    "credits": data["credits"],
                }
    return None
