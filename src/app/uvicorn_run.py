"""
Defines a function to run the FastAPI server using Uvicorn.

Imports uvicorn module.

Function:
- run_server(): Runs the FastAPI server using Uvicorn with specified host, port, and app instance.

"""
import uvicorn

def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_server()