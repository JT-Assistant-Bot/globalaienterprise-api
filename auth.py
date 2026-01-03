# auth.py

from enforcement import check_and_increment


class AuthError(Exception):
    """Raised when authentication or enforcement fails."""
    pass


def validate_request(headers: dict) -> None:
    """
    Validates API key presence and enforces usage limits.
    Raises AuthError if request should be blocked.
    """

    api_key = headers.get("X-API-Key")

    if not api_key or not isinstance(api_key, str):
        raise AuthError("API key missing or invalid")

    allowed = check_and_increment(api_key)

    if not allowed:
        raise AuthError("Free tier limit exceeded. Payment required.")
