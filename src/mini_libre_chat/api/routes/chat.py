"""
Chat API Route. This module defines the API route for handling chat requests.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from mini_libre_chat.llm.connector import AzureConnector
from mini_libre_chat.database.models import api
from mini_libre_chat.database.crud import _get_all_chats, save_chat
from mini_libre_chat.api.dependencies import get_db
from sqlalchemy.orm import Session
from mini_libre_chat.utils.logging import create_logger

import os
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


logger = create_logger("api.routes.chat")

router = APIRouter()
azure = AzureConnector(api_key=os.getenv("AZURE_OPENAI_API_KEY"))


chat_history = api.ChatCreate()
chat_history.add_prompt()


@router.post("/chat")
async def chat(data: api.UserMessage):
    chat_history.add_question(question=data.content)
    reply_text = azure.chat(chat_history.messages)
    chat_history.add_answer(answer=reply_text)

    return JSONResponse({"reply": reply_text, "chat_id": chat_history.id})


@router.get("/chats")
async def get_chats(db: Session = Depends(get_db)) -> list[api.ChatRead]:
    """
    Retrieve all chats from the database.

    Args:
        db: Database session dependency.

    Returns:
        A list of all chats stored in the database.
    """
    return _get_all_chats(db=db)


@router.post("/save_chat")
async def save_current_chat(db: Session = Depends(get_db)):
    """
    Save the current in-memory chat to the database.

    Args:
        db: Database session.

    Returns:
        JSONResponse: A confirmation message.
    """
    logger.info
    if len(chat_history.messages) == 0:
        raise HTTPException(status_code=400, detail="No chat history to save.")

    if chat_history.title is None:
        chat_with_title_question = chat_history.ask_for_title()
        generated_title = azure.chat(chat_with_title_question)
        chat_history.title = generated_title

    saved_chat_id = save_chat(db=db, chat=chat_history, chat_id=chat_history.id)
    chat_history.id = saved_chat_id  # Update in-memory chat ID to match saved chat

    return JSONResponse(
        {
            "message": "Chat saved successfully",
            "id": saved_chat_id,
            "title": chat_history.title,
        }
    )
