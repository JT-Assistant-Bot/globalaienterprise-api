# enforcement.py

from keys import check_and_consume

def check_and_increment(api_key: str) -> bool:
    """
    Central enforcement gate.
    Returns True if the request is allowed.
    Returns False if blocked (no credits / invalid key).
    """
    if not api_key or not isinstance(api_key, str):
        return False

    return check_and_consume(api_key)
