# config_utils.py
import os

def get_db_config() -> dict:
    db_config = {
        'DB_USERNAME': os.getenv('DB_USERNAME'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_NAME': os.getenv('DB_NAME')
    }
    print(db_config)
    print('hello')
    return db_config


