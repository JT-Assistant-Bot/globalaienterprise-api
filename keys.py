# keys.py

import json
import os
import secrets
import time
from typing import Dict

STORE_PATH = "api_keys.json"

# Default quotas
FREE_DAILY_LIMIT = 20


def _now() -> int:
    return int(time.time())


def _load_store() -> Dict:
    if not os.path.exists(STORE_PATH):
        return {}
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_store(store: Dict) -> None:
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)


def generate_api_key(prefix: str = "gae") -> str:
    """
    Generates a secure API key.
    """
    token = secrets.token_hex(16)
    return f"{prefix}_{token}"


def create_free_key() -> str:
    """
    Creates a free-tier API key with daily limits.
    """
    store = _load_store()
    key = generate_api_key("free")

    store[key] = {
        "type": "free",
        "daily_limit": FREE_DAILY_LIMIT,
        "used_today": 0,
        "reset_ts": _now() + 86400
    }

    _save_store(store)
    return key


def create_paid_key(credits: int) -> str:
    """
    Creates a paid API key with prepaid call credits.
    """
    store = _load_store()
    key = generate_api_key("paid")

    store[key] = {
        "type": "paid",
        "credits": credits,
        "created_ts": _now()
    }

    _save_store(store)
    return key


def check_and_consume(api_key: str) -> bool:
    """
    Validates key and consumes quota.
    Returns True if allowed, False otherwise.
    """
    store = _load_store()
    record = store.get(api_key)

    if not record:
        return False

    # Paid key logic
    if record["type"] == "paid":
        if record["credits"] <= 0:
            return False
        record["credits"] -= 1
        store[api_key] = record
        _save_store(store)
        return True

    # Free key logic
    if record["type"] == "free":
        now = _now()
        if now >= record["reset_ts"]:
            record["used_today"] = 0
            record["reset_ts"] = now + 86400

        if record["used_today"] >= record["daily_limit"]:
            return False

        record["used_today"] += 1
        store[api_key] = record
        _save_store(store)
        return True

    return False
