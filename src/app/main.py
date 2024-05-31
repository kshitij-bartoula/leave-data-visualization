"""
Configures FastAPI application and includes API routes.
"""
from fastapi import FastAPI
from app.scripts.api import router as api_router

app = FastAPI()

app.include_router(api_router)
