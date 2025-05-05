# auth_dep.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from backend.auth.database import get_db
from backend.auth.auth import verify_login  # adjust import if in same directory

security = HTTPBasic()

def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    username = credentials.username
    password = credentials.password

    if not verify_login(username, password, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username
