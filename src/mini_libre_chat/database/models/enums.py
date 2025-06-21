"""
sqlAlchemy enum for role
"""

__all__ = ["Role"]

import enum


class Role(str, enum.Enum):
    """Enum representing the role of a message sender in a chat."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
