"""This module can be used to run the actual fastapi server"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from mini_libre_chat.api.exceptions import validation_exception_handler
from mini_libre_chat.api.routes import chat, root


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")
app.include_router(chat.router)
app.include_router(root.router)
app.add_exception_handler(Exception, validation_exception_handler)
