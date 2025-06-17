"""
sqlAlchemy model for the Message entity.
"""

__all__ = ["Message", "MessageCreate", "MessageUpdate", "MessageRead"]

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from mini_libre_chat.database.schemas.enum import Role
from mini_libre_chat.database.engine import Base
from typing import Literal


class Message(Base):
    """SQLAlchemy model representing a message in a chat session."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)

    role = Column(SqlEnum(Role), nullable=False)

    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")


class MessageBase(BaseModel):
    """Base model for Message."""

    id: int
    role: Role
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    role: Literal["user", "assistant", "system"]
    content: str


class MessageUpdate(MessageBase):
    content: str


class MessageRead(MessageBase):
    pass
