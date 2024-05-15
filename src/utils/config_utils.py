# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
def get_db_config() -> dict:
    db_config = {
        'DB_USERNAME': os.getenv('DB_USERNAME'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_NAME': os.getenv('DB_NAME')
    }
    return db_config


