"""
database.py
Sets up the SQLAlchemy engine, SessionLocal, and Base for the Vercel Postgres DB.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read the database URL from environment variable (replace as needed)
DATABASE_URL = os.environ.get("VERCEL_POSTGRES_URL")

if not DATABASE_URL:
    # Handle the case where the env variable is not set
    # Provide a fallback or raise an error
    raise ValueError("No VERCEL_POSTGRES_URL found in environment variables.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured 'Session' class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db_session():
    """
    Dependency or helper function to provide a database session.
    Commonly used in frameworks like FastAPI, but useful for Flask as well.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
