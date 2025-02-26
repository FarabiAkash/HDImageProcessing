"""
test_database.py
Tests for database connectivity and basic CRUD operations.
"""

import os
import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from src.db.database import Base, engine, SessionLocal
from src.db.models import ImageMetadata

@pytest.fixture(scope='module')
def test_db_setup():
    """
    A fixture that:
      1) Ensures the Vercel Postgres URL is set.
      2) Creates all tables in the test database.
      3) Yields a session factory for tests.
      4) Optionally tears down tables at the end (if desired).
    """
    # 1) Check env var
    db_url = os.environ.get("VERCEL_POSTGRES_URL")
    if not db_url:
        raise RuntimeError("VERCEL_POSTGRES_URL is not set. Cannot run DB tests.")

    # 2) Create tables. If using migrations in production, 
    #    you might run them or create a temporary schema for testing.
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        raise RuntimeError(f"Could not create tables: {e}")

    # 3) Provide a session factory
    yield SessionLocal

    # 4) Cleanup - drop tables if you want a clean slate after tests
    #    Base.metadata.drop_all(bind=engine)


def test_connection_ok(test_db_setup):
    """
    Verifies that we can connect to the Vercel Postgres DB and create a session.
    """
    Session = test_db_setup  # from the fixture
    try:
        session = Session()
        # A simple query to confirm connection works
        result = session.execute("SELECT 1").fetchone()
        assert result[0] == 1
    finally:
        session.close()


def test_insert_image_metadata(test_db_setup):
    """
    Inserts a new ImageMetadata record and verifies it can be retrieved.
    """
    Session = test_db_setup
    session = Session()

    # Create a record
    test_image_id = "test_db_image"
    metadata_record = ImageMetadata(
        image_id=test_image_id,
        dtype="uint8",
        shape={"Z": 2, "T": 1, "C": 3, "Height": 4, "Width": 4}
    )
    session.add(metadata_record)
    session.commit()

    # Retrieve it
    retrieved = session.query(ImageMetadata).filter_by(image_id=test_image_id).first()
    session.close()

    assert retrieved is not None
    assert retrieved.image_id == test_image_id
    assert retrieved.dtype == "uint8"
    assert isinstance(retrieved.shape, dict)
    assert retrieved.shape["Z"] == 2


def test_no_duplicate_primary_key(test_db_setup):
    """
    Attempts to insert a record with a duplicate primary key (image_id).
    Expects an IntegrityError or similar.
    """
    from sqlalchemy.exc import IntegrityError

    Session = test_db_setup
    session = Session()

    record1 = ImageMetadata(
        image_id="duplicate_test",
        dtype="uint8",
        shape={"example": True}
    )
    record2 = ImageMetadata(
        image_id="duplicate_test",  # same primary key
        dtype="uint16",
        shape={"example": False}
    )

    session.add(record1)
    session.commit()

    # Adding a second record with the same PK should fail
    session.add(record2)
    with pytest.raises(IntegrityError):
        session.commit()

    # Roll back the failed transaction
    session.rollback()
    session.close()
