"""
This file contains constants.
"""

__all__ = [
    "SCHEMA",
    "DATABASE_URL",
    "DB_NAME",
]

SCHEMA = "chat_history"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
