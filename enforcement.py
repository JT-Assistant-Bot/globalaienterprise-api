# enforcement.py

from keys import check_and_consume


def check_and_increment(api_key: str) -> bool:
    """
    Wrapper used by API endpoints.
    """
    return check_and_consume(api_key)
