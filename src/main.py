import os
from fastapi import FastAPI
from app.api import router as api_router
from app.logging_config import configure_logging


# Configure logging
configure_logging()

# Create FastAPI app
app = FastAPI()

# Read environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
database_url = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
api_endpoint = os.getenv('API_ENDPOINT')
bearer_token = os.getenv('BEARER_TOKEN')

# Include API routers
app.include_router(api_router)
#testing cicd
