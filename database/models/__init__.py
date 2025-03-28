"""
Database Models for MedBlock

This module initializes all models for the MedBlock database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .user import User, Base as UserBase
from .record import MedicalRecord, AccessLog, Base as RecordBase

# Import config
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import DATABASE_URL

# Create engine and session
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create all tables
def init_db():
    """Initialize the database by creating all tables"""
    UserBase.metadata.create_all(engine)
    RecordBase.metadata.create_all(engine)
    print("Database tables created")

# Export models
__all__ = ['User', 'MedicalRecord', 'AccessLog', 'Session', 'init_db'] 