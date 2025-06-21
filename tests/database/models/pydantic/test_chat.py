"""
Test cases for chat schemas.
"""

from mini_libre_chat.database.models import enums, api


def test_add_prompt():
    chat = api.ChatCreate()
    chat.add_prompt("You are a test assistant.")
    assert len(chat.messages) == 1
    assert chat.messages[0].role == enums.Role.SYSTEM
    assert chat.messages[0].content == "You are a test assistant."


def test_add_question():
    chat = api.ChatCreate()
    chat.add_question("What is the capital of France?")
    assert chat.messages[0].role == enums.Role.USER
    assert "France" in chat.messages[0].content


def test_add_answer():
    chat = api.ChatCreate()
    chat.add_answer("The capital is Paris.")
    assert chat.messages[0].role == enums.Role.ASSISTANT
    assert "Paris" in chat.messages[0].content


def test_combined_conversation_flow():
    chat = api.ChatCreate()
    chat.add_prompt("You are a test assistant.")
    chat.add_question("Hello?")
    chat.add_answer("Hi there!")

    assert len(chat.messages) == 3
    assert chat.messages[0].role == enums.Role.SYSTEM
    assert chat.messages[1].role == enums.Role.USER
    assert chat.messages[2].role == enums.Role.ASSISTANT
