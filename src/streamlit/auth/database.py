import logging
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from utils.db_utils import connection

logger = logging.getLogger(__name__)

engine = connection()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

Base = declarative_base()
