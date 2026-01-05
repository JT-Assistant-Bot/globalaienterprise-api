# keys.py
# Central API key management (manual + Gumroad-compatible)

# In-memory store (Railway restart-safe is NOT required yet)
# Format:
# key: remaining_credits
API_KEYS = {
    "TEST-KEY-123": 1000,  # manual test key
}

def check_and_consume(api_key: str) -> bool:
    """
    Called on every protected request.
    Returns True if access is allowed.
    Decrements remaining credits.
    """
    if not api_key:
        return False

    if api_key not in API_KEYS:
        return False

    if API_KEYS[api_key] <= 0:
        return False

    API_KEYS[api_key] -= 1
    return True


def create_paid_key(api_key: str, credits: int = 1000) -> None:
    """
    Called by Gumroad webhook.
    Creates or overwrites a paid API key.
    """
    API_KEYS[api_key] = credits
