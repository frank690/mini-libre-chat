"""
sqlAlchemy model for the Message entity.
"""

__all__ = ["Message"]

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from mini_libre_chat.database.models.enums import Role
from mini_libre_chat.database.models.sqlalchemy.base import Base
from mini_libre_chat.database.constants import SCHEMA


class Message(Base):
    """SQLAlchemy model representing a message in a chat session."""

    __tablename__ = "message"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey(f"{SCHEMA}.chat.id"), nullable=False)
    role = Column(Enum(Role), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    chat = relationship("Chat", back_populates="messages")
