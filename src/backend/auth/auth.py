# auth_logic.py
import hashlib
from sqlalchemy.orm import Session
from utils.db_utils import get_result_from_query

def fetch_user_credentials(db: Session):
    """
    Fetches all username/password pairs from the user_accounts table.
    """
    query = "SELECT username, password FROM dw.user_accounts"
    return get_result_from_query(query, db)

def verify_login(username: str, password: str, db: Session) -> bool:
    """
    Verifies login credentials against stored, hashed credentials.
    """
    users = fetch_user_credentials(db)
    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    for db_username, db_password in users:
        if username == db_username and hashed_input == db_password:
            return True
    return False
