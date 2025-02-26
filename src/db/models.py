"""
models.py
Defines SQLAlchemy models (tables) for storing image metadata, analysis results, etc.
"""

import datetime
from sqlalchemy import Column, String, DateTime, JSON
from .database import Base

class ImageMetadata(Base):
    """
    Stores basic metadata about uploaded images.
    The 'image_id' matches what we generate upon upload.
    'shape' is stored as JSON to hold the 5D structure.
    """
    __tablename__ = 'image_metadata'

    image_id = Column(String, primary_key=True, index=True)
    dtype = Column(String, nullable=True)
    shape = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<ImageMetadata(image_id={self.image_id}, dtype={self.dtype}, shape={self.shape})>"
