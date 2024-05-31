"""
Configures FastAPI application and includes API routes.
"""
# from fastapi import FastAPI
# from app.scripts.api import router as api_router

# app = FastAPI()

# app.include_router(api_router)

from fastapi import FastAPI
from app.scripts.api import router as api_router
from app.scripts.api import refresh_data
import asyncio

app = FastAPI()

# Include the API router
app.include_router(api_router)

# Define startup event handler
@app.on_event("startup")
async def startup_event():
    # Start the background task to refresh data
    asyncio.create_task(refresh_data())

