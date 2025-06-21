"""
Test CRUD operations for chat functionality in the database.
"""

from mini_libre_chat.database.models import api, enums
from mini_libre_chat.database.crud import (
    _add_new_chat,
    _get_chat,
    _get_all_chats,
    _append_messages_to_chat,
)


def test_add_new_chat(session):
    chat_data = api.ChatCreate(title="Test Chat")
    chat_data.add_prompt("This is a test prompt.")
    chat_data.add_question("What is 2+2?")
    chat_data.add_answer("4")

    result = _add_new_chat(session, chat_data)

    assert isinstance(result, api.ChatRead)
    assert result.title == "Test Chat"
    assert hasattr(result, "id")
    assert isinstance(result.id, int)
    assert len(result.messages) == 3
    assert result.messages[0].role == enums.Role.SYSTEM
    assert result.messages[0].content == "This is a test prompt."
    assert result.messages[1].role == enums.Role.USER
    assert result.messages[1].content == "What is 2+2?"
    assert result.messages[2].role == enums.Role.ASSISTANT
    assert result.messages[2].content == "4"


def test_add_new_chat_with_empty_title(session):
    chat_data = api.ChatCreate()
    chat_data.add_prompt("This is a test prompt.")
    chat_data.add_question("What is 2+2?")
    chat_data.add_answer("4")

    result = _add_new_chat(session, chat_data)

    assert isinstance(result, api.ChatRead)
    assert result.title is None
    assert hasattr(result, "id")
    assert isinstance(result.id, int)
    assert len(result.messages) == 3
    assert result.messages[0].role == enums.Role.SYSTEM
    assert result.messages[0].content == "This is a test prompt."
    assert result.messages[1].role == enums.Role.USER
    assert result.messages[1].content == "What is 2+2?"
    assert result.messages[2].role == enums.Role.ASSISTANT
    assert result.messages[2].content == "4"


def test_add_new_chat_with_no_messages(session):
    chat_data = api.ChatCreate(title="Empty Chat")

    result = _add_new_chat(session, chat_data)

    assert isinstance(result, api.ChatRead)
    assert result.title == "Empty Chat"
    assert hasattr(result, "id")
    assert isinstance(result.id, int)
    assert len(result.messages) == 0


def test_get_chat(session):
    chat_data = api.ChatCreate(title="Test Chat for Retrieval")
    chat_data.add_prompt("This is a test prompt.")
    chat_data.add_question("What is 2+2?")
    chat_data.add_answer("4")

    created_chat = _add_new_chat(session, chat_data)
    retrieved_chat = _get_chat(session, created_chat.id)

    assert isinstance(retrieved_chat, api.ChatRead)
    assert retrieved_chat.id == created_chat.id
    assert retrieved_chat.title == "Test Chat for Retrieval"
    assert len(retrieved_chat.messages) == 3
    assert retrieved_chat.messages[0].role == enums.Role.SYSTEM
    assert retrieved_chat.messages[0].content == "This is a test prompt."
    assert retrieved_chat.messages[1].role == enums.Role.USER
    assert retrieved_chat.messages[1].content == "What is 2+2?"
    assert retrieved_chat.messages[2].role == enums.Role.ASSISTANT
    assert retrieved_chat.messages[2].content == "4"


def test_get_non_existent_chat(session):
    retrieved_chat = _get_chat(session, 1337)
    assert retrieved_chat is None


def test_get_all_chats(session):
    chat1 = api.ChatCreate(title="Chat 1")
    chat1.add_prompt("Prompt 1")
    chat1.add_question("Question 1")
    chat1.add_answer("Answer 1")

    chat2 = api.ChatCreate(title="Chat 2")
    chat2.add_prompt("Prompt 2")
    chat2.add_question("Question 2")
    chat2.add_answer("Answer 2")

    _add_new_chat(session, chat1)
    _add_new_chat(session, chat2)

    all_chats = _get_all_chats(session)

    assert isinstance(all_chats, list)
    assert len(all_chats) >= 2
    assert any(chat.title == "Chat 1" for chat in all_chats)
    assert any(chat.title == "Chat 2" for chat in all_chats)


def test_get_all_chats_empty(session):
    all_chats = _get_all_chats(session)
    assert isinstance(all_chats, list)
    assert len(all_chats) == 0


def test_append_messages_to_chat(session):
    chat_data = api.ChatCreate(title="Chat to Append")
    chat_data.add_prompt("Initial prompt.")
    chat_data.add_question("Initial question?")
    chat_data.add_answer("Initial answer.")

    created_chat = _add_new_chat(session, chat_data)

    chat_data.add_question("Follow-up question?")
    chat_data.add_answer("Follow-up answer.")

    new_messages = chat_data.messages[3:]  # Get the new messages to append

    _append_messages_to_chat(
        db=session, chat_id=created_chat.id, new_messages=new_messages
    )

    updated_chat = _get_chat(session, created_chat.id)
    assert isinstance(updated_chat, api.ChatRead)
    assert updated_chat.id == created_chat.id
    assert len(updated_chat.messages) == 5
    assert updated_chat.messages[3].role == enums.Role.USER
    assert updated_chat.messages[3].content == "Follow-up question?"
    assert updated_chat.messages[4].role == enums.Role.ASSISTANT
    assert updated_chat.messages[4].content == "Follow-up answer."
