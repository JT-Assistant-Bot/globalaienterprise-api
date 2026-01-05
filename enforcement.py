"""
enforcement.py
Request enforcement layer for GlobalAIEnterprise Shield.
"""

from typing import Optional
from keys import check_and_consume


def check_and_increment(api_key: Optional[str]) -> bool:
    """
    Validate API key and consume one credit.

    Returns:
        True  -> request allowed
        False -> request denied
    """
    return check_and_consume(api_key)
