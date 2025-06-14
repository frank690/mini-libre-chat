"""
Contains the database engine.
"""

__all__ = ["Base", "engine", "session_maker"]


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from mini_libre_chat.database.constants import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine)
