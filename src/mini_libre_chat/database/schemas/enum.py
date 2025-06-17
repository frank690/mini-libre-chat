"""
sqlAlchemy enum for role
"""

__all__ = ["Role"]

import enum


class Role(enum.Enum):
    """Enum representing the role of a message sender in a chat."""

    USER = "user"
    ASSISTANT = "assistant"
