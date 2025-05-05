# # """
# # Configures FastAPI application and includes API routes.
# # """
# # from fastapi import FastAPI
# # from backend.scripts.api import router as api_router

# # app = FastAPI()

# # app.include_router(api_router)

# """
# Main entry point for FastAPI application.
# Configures and runs the app with included API routes.
# """

# from fastapi import FastAPI
# from backend.scripts.api import router as api_router
# import uvicorn

# app = FastAPI()

# # Include your API routes
# app.include_router(api_router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# app.py
from fastapi import FastAPI, Depends
from backend.scripts.api import router as api_router
from backend.auth.auth_dep import authenticate_user  # adjust path accordingly
import uvicorn

app = FastAPI(dependencies=[Depends(authenticate_user)])

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
