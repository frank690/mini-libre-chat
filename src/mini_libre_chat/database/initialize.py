"""
This file contains functionality to initialize the database, schema and tables.
"""

__all__ = ["create_schema_and_tables", "drop_schema"]


from sqlalchemy import text

from mini_libre_chat.database.constants import SCHEMA
from mini_libre_chat.database.engine import engine, Base
from mini_libre_chat.utils import create_logger


logger = create_logger(__name__)


def create_schema_and_tables() -> bool:
    """
    Creates the schema and tables in the database.

    Args:
        engine: The SQLAlchemy engine to connect to the database.

    Returns:
        Flag to indicate if process was successful.
    """
    logger.info(f"Creating schema: {SCHEMA}")

    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))

        Base.metadata.schema = SCHEMA
        Base.metadata.create_all(engine)
        logger.info("Database schema and tables created successfully.")
        return True

    except Exception as e:
        logger.error(f"Failed creating schema and tables: {e}")
        return False


def drop_schema(confirmation: bool = False) -> bool:
    """
    Drops all tables and the schema.

    Args:
        confirmation: Needs to be explicitly set true, otherwise function will not do anything.

    Returns:
        Flag to indicate if process was successful.
    """
    if confirmation is False:
        logger.warning(
            f"DROPPING SCHEMA AND TABLES REQUIRES CONFIRMATION FLAG TO BE TRUE.\n ARE YOU SURE YOU WANT TO DELETE: {SCHEMA}"
        )
        return False

    logger.info(f"Dropping schema: {SCHEMA}")
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DROP SCHEMA {SCHEMA} CASCADE"))

        logger.info("Dropping of schema and all table was successfull")
        return True

    except Exception as e:
        logger.error(f"Failed dropping schema and tables: {e}")
        return False
