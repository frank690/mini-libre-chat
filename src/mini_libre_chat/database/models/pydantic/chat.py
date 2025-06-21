"""
pydantic models for the Chat entity.
"""

__all__ = ["ChatCreate", "ChatRead"]

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from mini_libre_chat.database.models.pydantic.message import MessageCreate, MessageRead


class ChatBase(BaseModel):
    """Base model for Chat."""

    title: Optional[str] = None
    messages: List[MessageCreate] = []

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ChatCreate(ChatBase):
    """For creating a new chat session (input only)."""

    id: Optional[int] = None

    def add_prompt(self, prompt: str = "You are a helpful assistant.") -> None:
        self.messages.append(MessageCreate(role="system", content=prompt))

    def add_question(self, question: str) -> None:
        """
        Add the given user question to the chat history
        """
        self.messages.append(MessageCreate(role="user", content=question))

    def add_answer(self, answer: str) -> None:
        """
        Add the given model answer to the chat history
        """
        self.messages.append(MessageCreate(role="assistant", content=answer))


class ChatRead(ChatBase):
    id: int
    messages: List[MessageRead]
