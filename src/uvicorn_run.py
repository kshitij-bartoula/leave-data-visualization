import os
import uvicorn

#port=int(os.getenv("PORT", 8000))

def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_server()