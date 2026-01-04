# keys.py

import uuid

# In-memory store
# key: (email, license_key)
# value: { api_key, credits }
ISSUED_KEYS = {}

# Reverse lookup for enforcement
# key: api_key
# value: (email, license_key)
API_KEY_INDEX = {}


def create_paid_key(credits: int, email: str, license_key: str) -> str:
    api_key = str(uuid.uuid4())

    ISSUED_KEYS[(email, license_key)] = {
        "api_key": api_key,
        "credits": credits
    }

    API_KEY_INDEX[api_key] = (email, license_key)
    return api_key


def get_key(email: str, license_key: str):
    return ISSUED_KEYS.get((email, license_key))


def check_and_consume(api_key: str) -> bool:
    """
    Validates API key and consumes 1 credit.
    """
    identity = API_KEY_INDEX.get(api_key)
    if not identity:
        return False

    record = ISSUED_KEYS.get(identity)
    if not record:
        return False

    if record["credits"] <= 0:
        return False

    record["credits"] -= 1
    return True
