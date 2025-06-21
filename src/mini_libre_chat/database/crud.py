"""
This module contains CRUD operations for the database.
"""

__all__ = [
    "_add_new_chat",
    "_get_chat",
    "_get_all_chats",
    "save_chat",
    "_append_messages_to_chat",
]

from sqlalchemy.orm import Session
from mini_libre_chat.database.models import sql, api
from mini_libre_chat.utils.logging import create_logger

logger = create_logger("crud")


def _add_new_chat(db: Session, chat: api.ChatCreate) -> int:
    """
    Add a given chat to the database.

    Args:
        db: Database instance
        chat: Instance of api.ChatCreate containing chat data.

    Returns:
        int: The ID of the created chat.
    """
    new_chat = sql.Chat(
        title=chat.title,
    )

    try:
        db.add(new_chat)
        db.flush()  # Ensure the chat ID is generated before adding messages

        for message in chat.messages:
            new_message = sql.Message(
                chat=new_chat, role=message.role, content=message.content
            )
            db.add(new_message)

        db.commit()
        db.refresh(new_chat)  # Ensures new_chat.messages is populated
        logger.info(f"Added chat: {chat.title}.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add chat '{chat.title}': {e}")
        raise

    return new_chat.id


def _get_chat(db: Session, chat_id: int) -> api.ChatRead | None:
    """
    Retrieve a chat by its ID.

    Args:
        db: Database instance
        chat_id: ID of the chat to retrieve.

    Returns:
        api.ChatRead or None: The chat instance if found, otherwise None.
    """
    chat = db.query(sql.Chat).filter(sql.Chat.id == chat_id).first()

    if chat:
        logger.info(f"Retrieved chat with ID {chat_id}.")
        return api.ChatRead.model_validate(chat)

    logger.warning(f"Chat with ID {chat_id} not found.")
    return None


def _get_all_chats(db: Session) -> list[api.ChatRead]:
    """
    Retrieve all chats from the database.

    Args:
        db: Database instance

    Returns:
        list[api.ChatRead]: List of all chat instances.
    """
    chats = db.query(sql.Chat).all()
    logger.info(f"Retrieved {len(chats)} chats from the database.")
    return [api.ChatRead.model_validate(chat) for chat in chats]


def save_chat(db: Session, chat: api.ChatCreate, chat_id: int | None = None) -> int:
    """
    Save a chat to the database. If chat_id is given, append new messages to the existing chat.

    Args:
        db: SQLAlchemy session.
        chat: ChatCreate with messages.
        chat_id: ID of the existing chat to update, if any.

    Returns:
        int: The ID of the chat after saving.
    """
    if chat_id is not None:
        return _append_messages_to_chat(
            db=db, chat_id=chat_id, new_messages=chat.messages
        )

    return _add_new_chat(db=db, chat=chat)


def _append_messages_to_chat(
    db: Session, chat_id: int, new_messages: list[api.MessageCreate]
) -> int:
    """
    Append messages to an existing chat.

    Args:
        db: Database instance
        chat_id: ID of the existing chat to append messages to.
        new_messages: List of new messages to append.

    Returns:
        int: The ID of the chat after appending messages.
    """
    for msg in new_messages:
        db.add(sql.Message(chat_id=chat_id, role=msg.role, content=msg.content))

    db.commit()
    logger.info(f"Appended {len(new_messages)} new messages to chat with ID {chat_id}.")
    return chat_id
