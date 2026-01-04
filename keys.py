# keys.py

import uuid

# In-memory store (OK for now; can be upgraded later)
ISSUED_KEYS = {}

def create_paid_key(credits: int, email: str, license_key: str) -> str:
    api_key = str(uuid.uuid4())
    ISSUED_KEYS[(email, license_key)] = {
        "api_key": api_key,
        "credits": credits
    }
    return api_key

def get_key(email: str, license_key: str):
    return ISSUED_KEYS.get((email, license_key))
