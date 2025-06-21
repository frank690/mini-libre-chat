"""
pydantic model for the Message entity.
"""

__all__ = ["UserMessage", "MessageCreate", "MessageRead"]

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from mini_libre_chat.database.models import enums


class UserMessage(BaseModel):
    """Pydantic model for user messages."""

    content: str


class MessageBase(BaseModel):
    """Base Pydantic model for shared message fields."""

    role: enums.Role
    content: str

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class MessageCreate(MessageBase):
    """For creating a new message (input only)."""

    pass


class MessageRead(MessageBase):
    """For returning a message from the database."""

    id: int
    chat_id: int
    timestamp: datetime
