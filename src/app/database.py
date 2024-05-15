import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.db_utils import connection


logger = logging.getLogger(__name__)

# Create engine and session
engine = connection()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# Base class for declarative models
Base = declarative_base()
