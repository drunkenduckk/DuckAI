from __future__ import annotations
import os, sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Make sure imports from app/src work whether we run as a module or with uvicorn
BASE_DIR = Path(__file__).resolve().parents[1]  # points to .../app
SRC_DIR = BASE_DIR / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.clients.openrouter_client import OpenRouterClient
from src.router import route
from src.local_kb import lookup

app = FastAPI(title="Ready AI Router")

static_dir = Path(__file__).resolve().parent / "static"
templates_dir = Path(__file__).resolve().parent / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

class ChatRequest(BaseModel):
    message: str

_client = None
def get_client() -> OpenRouterClient:
    global _client
    if _client is None:
        _client = OpenRouterClient()
    return _client

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(req: ChatRequest):
    user_msg = (req.message or "").strip()
    if not user_msg:
        return JSONResponse({"reply": "Say something first.", "route": "local", "reason": "Empty input."})
    path, reason = route(user_msg)
    if path == "local":
        reply = lookup(user_msg) or "I don't know that locally. Try asking a fuller question."
    elif path == "gpt":
        reply = get_client().chat([{"role": "user", "content": user_msg}])
    else:
        reply = (
            "This looks like live data (flights, prices, news, weather, etc.). "
            "I don’t have real-time access yet. "
            "Integrate a provider API or refine your question."
        )
    return JSONResponse({"reply": reply, "route": path, "reason": reason})