"""
Contains the database engine.
"""

__all__ = ["Base", "Engine", "Session"]


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from mini_libre_chat.database.constants import DATABASE_URL

Engine = create_engine(DATABASE_URL)  # for more details use: , echo=True, future=True)
Session = sessionmaker(bind=Engine)
Base = declarative_base()
