"""
Configures FastAPI application and includes API routes.
"""
from fastapi import FastAPI
from app.scripts.api import router as api_router

app = FastAPI()

app.include_router(api_router)

# from fastapi import FastAPI
# from app.scripts.api import router as api_router
# from app.scripts.api import router as api_router, startup_event
# import asyncio

# app = FastAPI()

# # Include the API router
# app.include_router(api_router)

# # Register the startup event handler
# app.add_event_handler("startup", startup_event)

