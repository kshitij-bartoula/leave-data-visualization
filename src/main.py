from fastapi import FastAPI
from app.api import router as api_router
from app.logging_config import configure_logging


# Configure logging
configure_logging()

# Create FastAPI app
app = FastAPI()

# Include API routers
app.include_router(api_router)
#testing cicd
