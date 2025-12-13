from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from dotenv import load_dotenv
import uvicorn
import os
import time

load_dotenv()

EMAIL = os.getenv("EMAIL") 
SECRET = os.getenv("SECRET")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
START_TIME = time.time()

@app.get("/")
def root():
    return {
        "message": "LLM Quiz Agent API",
        "endpoints": ["/healthz", "/solve", "/docs"],
        "uptime_seconds": int(time.time() - START_TIME)
    }

@app.get("/healthz")
def healthz():
    """Simple liveness check."""
    return {
        "status": "ok",
        "uptime_seconds": int(time.time() - START_TIME)
    }


async def _handle_quiz_request(request: Request, background_tasks: BackgroundTasks):
    """Validate incoming payload, enforce secret, and start the agent."""
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    url = data.get("url")
    secret = data.get("secret")
    email = data.get("email") or EMAIL

    if not url or not secret:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not SECRET:
        raise HTTPException(status_code=500, detail="Server secret not configured")

    if secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    payload = dict(data)
    if email:
        payload["email"] = email

    print(f"Verified request. Starting quiz task for {url}...")
    background_tasks.add_task(run_agent, payload)

    return JSONResponse(status_code=200, content={"status": "ok"})


@app.post("/")
async def solve_root(request: Request, background_tasks: BackgroundTasks):
    return await _handle_quiz_request(request, background_tasks)


@app.post("/solve")
async def solve(request: Request, background_tasks: BackgroundTasks):
    return await _handle_quiz_request(request, background_tasks)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)