"""
sqlAlchemy models for the Chat entity.
"""

__all__ = ["Chat"]

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from mini_libre_chat.database.models.sqlalchemy.base import Base
from mini_libre_chat.database.constants import SCHEMA


class Chat(Base):
    """SQLAlchemy model representing a chat session."""

    __tablename__ = "chat"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
