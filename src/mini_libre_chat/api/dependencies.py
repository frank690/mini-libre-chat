"""
Database Dependencies. This module provides database-related dependencies for the API.
"""

__all__ = ["get_db"]

from mini_libre_chat.database.models import sql
from sqlalchemy.orm import Session
from typing import Generator


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.
    Closes it automatically after the request.
    """
    db = sql.Session()
    try:
        yield db
    finally:
        db.close()
