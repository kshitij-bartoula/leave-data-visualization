import logging
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from utils.db_utils import connection  # assumes you return SQLAlchemy engine from here

logger = logging.getLogger(__name__)

# Create engine
engine = connection()

# Create session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for DB session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for models
Base = declarative_base()
