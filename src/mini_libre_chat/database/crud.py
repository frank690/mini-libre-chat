"""
This module contains CRUD operations for the database.
"""

__all__ = ["_get_chat", "_add_chat"]

from sqlalchemy.orm import Session
from mini_libre_chat.database.schemas.chat import ChatCreate, ChatRead, Chat

from mini_libre_chat.utils.logging import create_logger

logger = create_logger("crud")


def _get_chat(db: Session, chat_id: int) -> ChatRead:
    """
    Get a chat from the database.
    Args:
        db: session with db
        chat_id: ID of the chat to retrieve

    Returns:
        The chat as a Pydantic schema
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    return ChatRead.model_validate(chat)


def _add_chat(db: Session, chat: ChatCreate) -> ChatRead:
    """
    Initialize a Chat class instance with the given data.
    Add the instance to the database.

    Args:
        db: Session with database.
        chat: Chat data.

    Returns:
        New chat data.
    """
    new_chat = Chat(**chat.model_dump())
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return ChatRead.model_validate(new_chat)
