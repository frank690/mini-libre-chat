"""
sqlAlchemy model for the Chat entity.
"""

__all__ = ["Chat", "ChatCreate", "ChatRead"]

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from mini_libre_chat.database.engine import Base
from typing import Optional, List
from mini_libre_chat.database.schemas.message import MessageRead


class Chat(Base):
    """SQLAlchemy model representing a chat session."""

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )


class ChatBase(BaseModel):
    """Base model for Chat."""

    id: int
    title: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    messages: List[MessageRead] = []
