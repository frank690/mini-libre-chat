"""This file contains fixtures for database testing."""

import pytest
from mini_libre_chat.database.models import sql
from mini_libre_chat.database.constants import DATABASE_URL, SCHEMA
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine


@pytest.fixture(scope="function")
def session():
    print("Setting up test database session...")
    TEST_DATABASE_URL = DATABASE_URL + "_test"

    engine = create_engine(TEST_DATABASE_URL)
    connection = engine.connect()

    transaction = connection.begin()
    connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))

    # Bind the Base metadata to the connection, not just the engine
    sql.Base.metadata.create_all(bind=connection)

    # Create session using the same connection
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()  # Roll back everything for isolation
    connection.close()
