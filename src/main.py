from fastapi import FastAPI
from app.api import router as api_router

# Create FastAPI app
app = FastAPI()

# Include API routers
app.include_router(api_router)
