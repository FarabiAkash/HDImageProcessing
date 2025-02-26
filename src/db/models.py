from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    dimensions = Column(String, nullable=False)  # Stored as JSON string
    upload_date = Column(DateTime, default=datetime.utcnow)
    
class Statistics(Base):
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, nullable=False)
    mean = Column(Float)
    std = Column(Float)
    min = Column(Float)
    max = Column(Float)
