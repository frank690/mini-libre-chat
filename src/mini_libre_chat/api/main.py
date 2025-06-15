"""This module can be used to run the actual fastapi server"""

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from mini_libre_chat.database import session_maker
from mini_libre_chat.utils import create_logger
from mini_libre_chat.llm import AzureConnector

logger = create_logger("main")
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

azure = AzureConnector(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


def get_database_connection():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    message: str = ""


class ChatHistory(BaseModel):
    messages: list[dict] = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    def add_question(self, question: str) -> None:
        """
        Add the given user question to the chat history
        """
        self.messages.append({"role": "user", "content": question})

    def add_answer(self, answer: str) -> None:
        """
        Add the given model answer to the chat history
        """
        self.messages.append({"role": "assistant", "content": answer})


chat_history = ChatHistory()


@app.get("/")
def root():
    return RedirectResponse(url="/app")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.exception(f"validation exception: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.post("/chat")
async def chat(data: ChatRequest):
    chat_history.add_question(question=data.message)

    reply_chunks = []
    for chunk in azure.chat(chat_history.messages):
        reply_chunks.append(chunk)
    reply_text = "".join(reply_chunks)

    chat_history.add_answer(answer=reply_text)
    return JSONResponse({"reply": reply_text})
